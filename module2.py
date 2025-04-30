from utils import imageType
import module1
from FA_class import DFA
import module4

def solve(json_str: str, image: imageType) -> bool:
    
    json_to_img = module4.solve(json_str, len(image))
    
    same_num = 0
    
    
    for i in range(len(image)):
        for j in range(len(image[0])):
            if image[i][j] == json_to_img[i][j]:
                same_num += 1
                
    
    similarity_ratio = same_num / (len(image) * len(image[0]))
    
    
    if similarity_ratio > 0.8:
        return True
    else:
        return False

if __name__ == "__main__":
    
    print(
        solve(
            '{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_3"], '
            '"alphabet": ["0", "1", "2", "3"], "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"}, "q_1": {"0": '
            '"q_3", "1": "q_3", "2": "q_3", "3": "q_4"}, "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"}, '
            '"q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"}, "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", '
            '"3": "q_4"}}',
            [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]
        )
    )
