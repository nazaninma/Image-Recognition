from utils import imageType
import module1
from FA_class import DFA
import module4


def get_percent(json_str: str, image: imageType) -> float:
    
    json_to_img = module4.solve(json_str, len(image))
    
    same_num = 0
    
    
    for i in range(len(image)):
        for j in range(len(image[0])):
            if image[i][j] == json_to_img[i][j]:
                same_num += 1
                
    
    similarity_ratio = same_num / (len(image) * len(image[0]))
    
    return similarity_ratio


def solve(json_fa_list: list[str], images: list[imageType]) -> list[int]:
    result = []
    
    for image in images:
        max_similarity = 0
        max_similarity_index = 0
        
        for j, json_str in enumerate(json_fa_list):
            percent = get_percent(json_str, image)
            if percent > max_similarity:
                max_similarity = percent
                max_similarity_index = j
        
        result.append(max_similarity_index)
    
    return result


if __name__ == "__main__":
    
    pass
