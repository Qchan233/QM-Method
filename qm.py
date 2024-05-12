
def compare_tuple(tup1, tup2):
    assert len(tup1) == len(tup2)

    res = []
    diff_count = 0
    for t1, t2 in zip(tup1, tup2): 
        if t1 != t2:
            diff_count += 1
            res.append('-')
        else:
            res.append(t1)

        if diff_count > 1:
            return None
    
    assert diff_count == 1
    return res

class minimizer:
    def __init__(self, ndigits) -> None:
        self.ndigits = ndigits
        self.alphabets = [chr(i) for i in range(65, 65 + ndigits)]
    

    def minimize(self, sops, notcares):
        assert max(sops) < 2 ** self.ndigits;
        assert max(notcares) < 2 ** self.ndigits;

        assert len

        total = sops + notcares

        def int_to_binary_list(number, n):
            # 获取整数的二进制表示，去掉前面的'0b'
            binary_str = bin(number)[2:]
            # 如果二进制字符串长度小于n，使用前导'0'补足
            if len(binary_str) < n:
                binary_str = binary_str.zfill(n)
            # 将每个字符（'0'或'1'）转换为int，然后放入列表
            binary_list = [int(bit) for bit in binary_str]
            return tuple(binary_list)        

        initial_dict = {frozenset([t]): int_to_binary_list(t, self.ndigits) for t in total}

        def find_primes(initial_dict):
            stage = 0
            need_merge = True
            primes = set()
            prime_dict = {}
            # We could use inplace, just for the sake of clarity
            implicants = initial_dict.copy()

            while need_merge:
                need_merge = False

                num_1_buckets = [[] for _ in range(self.ndigits + 1)]
                for key, value in implicants.items():
                    num_1_buckets[value.count(1)].append(key)
                
                has_merged = {}
                next_implicants = {}
                
                for n_ones in range(self.ndigits - stage):
                    for i in num_1_buckets[n_ones]:
                        for j in num_1_buckets[n_ones + 1]:
                            impl = compare_tuple(implicants[i], implicants[j])
                            if impl:
                                need_merge = True
                                next_implicants[i | j] = impl
                                has_merged[i] = True
                                has_merged[j] = True

                not_merged = [key for key in implicants.keys() if not has_merged.get(key)]
                primes.update(not_merged)

                for key in not_merged:
                    prime_dict[key] = implicants[key]
                
                implicants = next_implicants
                stage += 1
            return primes, prime_dict


        _, prime_dict = find_primes(initial_dict)
        return prime_dict
    
    def inplicant_name(self, inplicant):
        assert len(inplicant) == self.ndigits
        res = ' '
        for i, c in enumerate(inplicant):
            if c == '1':
                res += self.alphabets[i]
            elif c == '0':
                res += '\u0305' + self.alphabets[i]
            else:
                assert c == '-'

        res += ' '
        return res 

if __name__ == '__main__':
    minimizer = minimizer(4)

    print(minimizer.minimize([4,8,10,11,12,15], [9,14]))
