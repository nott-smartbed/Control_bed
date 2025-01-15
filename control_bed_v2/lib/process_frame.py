# Xử lý dữ liệu dùng để chuyển input dạng string sang list
def process_input(input_str):
    # Chuyển chuỗi thành list
    input_list = eval(input_str)

    output_list = []
    for item in input_list:
        if item == 'on':
            output_list.append(1)
        elif item == 'off':
            output_list.append(0)
        else:
            try:
                # Chuyển đổi các giá trị số dưới dạng chuỗi thành int (số nguyên)
                output_list.append(int(float(item)))  # Chuyển thành float trước, sau đó chuyển thành int
            except ValueError:
                # Nếu không thể chuyển đổi thành int, giữ nguyên chuỗi
                output_list.append(item)

    return output_list