#模糊查询工具类
import re
class FuzzyMatch:
    @classmethod
    def fuzzyFinder(cls,user_input, collection):
        suggestions = []
        if user_input=='':
            return None
        else:
            pattern = '.*'.join(user_input)  # Converts 'djm' to 'd.*j.*m'
            regex = re.compile(pattern)  # Compiles a regex.
            for item in collection:
                match = regex.search(str(item))  # Checks if the current item matches the regex.
                if match:
                    suggestions.append(item)
            return suggestions

#测试
if __name__ == '__main__':
    collection = ['妊娠合并',
                  '妊娠合并2',
                  '妊娠合并4',
                  '妊娠合并5',
                  '治疗方案六',
                  '治疗方案七',
                  ]
    print(FuzzyMatch.fuzzyFinder('', collection))
