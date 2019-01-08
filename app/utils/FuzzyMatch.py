#模糊查询工具类
import re
class FuzzyMatch:
    @classmethod
    def fuzzyFinder(cls,user_input, collection):
        suggestions = []
        pattern = '.*'.join(user_input)  # Converts 'djm' to 'd.*j.*m'
        regex = re.compile(pattern)  # Compiles a regex.
        for item in collection:
<<<<<<< HEAD
            match = regex.search(item)  # Checks if the current item matches the regex.
=======
            match = regex.search(str(item))  # Checks if the current item matches the regex.
>>>>>>> 徐煜涵
            if match:
                suggestions.append(item)
        return suggestions

#测试
if __name__ == '__main__':
    collection = ['治疗方案一',
                  '治疗方案二',
                  '治疗方案三',
                  '治疗方案五',
                  '治疗方案六',
                  '治疗方案七',
                  ]
    print(FuzzyMatch.fuzzyFinder('疗', collection))
