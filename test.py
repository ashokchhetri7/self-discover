from self_discover import SelfDiscover
from task_example import task1

result = SelfDiscover(task=task1)


result()

print(f"SELECTED_MODULES : {result.selected_modules}")
print(f"ADAPTED_MODULES : {result.adapted_modules}")
print(f"REASONING_STRUCTURE : {result.reasoning_structure}")
print(f"SOLUTION: {result.solution}")
