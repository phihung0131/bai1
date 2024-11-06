# Định nghĩa một lớp NPuzzleState để biểu diễn trạng thái của n-puzzle
class NPuzzleState:
    def __init__(self, board, blank_pos):
        # board: danh sách biểu diễn trạng thái của bảng, với 0 là ô trống
        # blank_pos: vị trí của ô trống trên bảng
        self.board = board
        self.blank_pos = blank_pos

    def __hash__(self):
        # Hàm băm để lưu trữ trạng thái trong tập hợp visited
        return hash(tuple(self.board))

    def __eq__(self, other):
        # So sánh hai trạng thái để kiểm tra tính tương đương
        return self.board == other.board

# Hàm kiểm tra xem trạng thái hiện tại có phải là trạng thái đích không
def is_goal_state(state):
    # Trạng thái đích: [1, 2, 3, ..., N*N-1, 0]
    goal_board = list(range(1, len(state.board))) + [0]
    return state.board == goal_board

# Hàm lấy danh sách các nước đi hợp lệ cho ô trống
def get_valid_moves(state, N):
    moves = []
    x, y = divmod(state.blank_pos, N)  # Tính hàng (x) và cột (y) từ vị trí của ô trống

    # Kiểm tra và thêm các nước đi hợp lệ
    if x > 0:  # Di chuyển lên trên
        moves.append(('Up', (x - 1) * N + y))
    if x < N - 1:  # Di chuyển xuống dưới
        moves.append(('Down', (x + 1) * N + y))
    if y > 0:  # Di chuyển sang trái
        moves.append(('Left', x * N + (y - 1)))
    if y < N - 1:  # Di chuyển sang phải
        moves.append(('Right', x * N + (y + 1)))

    return moves

# Hàm thực hiện một nước đi và trả về trạng thái mới sau khi di chuyển ô trống
def apply_move(state, move):
    direction, new_blank_pos = move  # Lấy hướng di chuyển và vị trí mới của ô trống
    new_board = state.board[:]       # Sao chép bảng hiện tại

    # Đổi chỗ ô trống với ô mới
    new_board[state.blank_pos], new_board[new_blank_pos] = new_board[new_blank_pos], new_board[state.blank_pos]
    
    return NPuzzleState(new_board, new_blank_pos)

# Thuật toán DFS để tìm lời giải cho n-puzzle
def dfs(initial_state, N, max_depth=1000):
    # stack lưu trữ các trạng thái cần khám phá, path là danh sách nước đi, depth là độ sâu hiện tại
    stack = [(initial_state, [], 0)]
    visited = set()  # Tập hợp các trạng thái đã duyệt

    # Vòng lặp chính của DFS
    while stack:
        state, path, depth = stack.pop()

        # Kiểm tra trạng thái đích trước khi kiểm tra visited
        if is_goal_state(state):
            return path  # Trả về đường đi nếu đã đến trạng thái đích

        # Kiểm tra nếu độ sâu vượt quá giới hạn hoặc đã duyệt trạng thái này
        if depth > max_depth or state in visited:
            continue  # Bỏ qua nếu vượt quá độ sâu hoặc trạng thái đã duyệt
        
        visited.add(state)  # Đánh dấu trạng thái đã duyệt
        
        # Lấy các nước đi hợp lệ và duyệt từng nước đi
        valid_moves = get_valid_moves(state, N)
        for move in valid_moves:
            new_state = apply_move(state, move)
            if new_state not in visited:
                # Thêm trạng thái mới vào stack với độ sâu tăng thêm 1
                stack.append((new_state, path + [move[0]], depth + 1))
    
    return None  # Trả về None nếu không tìm thấy lời giải