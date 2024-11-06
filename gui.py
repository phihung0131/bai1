import tkinter as tk
from tkinter import ttk, messagebox
from n_puzzle import NPuzzleState, dfs, get_valid_moves, apply_move
import random

# Lớp giao diện đồ họa cho trò chơi N-Puzzle
class NPuzzleGUI:
    def __init__(self, root):
        # Khởi tạo cửa sổ chính và thiết lập tiêu đề
        self.root = root
        self.root.title("N-Puzzle Solver")
        
        # Khung nhập dữ liệu
        input_frame = ttk.Frame(root, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Nhập giá trị N (kích thước bảng)
        ttk.Label(input_frame, text="Enter N:").grid(row=0, column=0, padx=5)
        self.n_var = tk.StringVar(value="3")  # Mặc định là 3x3
        self.n_entry = ttk.Entry(input_frame, textvariable=self.n_var, width=10)
        self.n_entry.grid(row=0, column=1, padx=5)
        
        # Nút "Generate Puzzle" để tạo bảng xếp ngẫu nhiên
        ttk.Button(input_frame, text="Generate Puzzle", command=self.generate_puzzle).grid(row=0, column=2, padx=5)
        # Nút "Solve" để giải câu đố
        ttk.Button(input_frame, text="Solve", command=self.solve_puzzle).grid(row=0, column=3, padx=5)
        
        # Khung chứa các ô của bảng
        self.puzzle_frame = ttk.Frame(root, padding="10")
        self.puzzle_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.buttons = []  # Lưu các nút của bảng
        self.current_state = None  # Trạng thái hiện tại của bảng

        # Khung hiển thị trạng thái đích
        self.goal_frame = ttk.LabelFrame(root, text="Goal State", padding="10")
        self.goal_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.goal_buttons = []

    # Hàm tạo bảng xếp ngẫu nhiên
    def generate_puzzle(self):
        try:
            N = int(self.n_var.get())
            if N < 2:
                raise ValueError("N must be at least 2")
                
            # Xóa các nút hiện có (nếu có)
            for button in self.buttons:
                button.destroy()
            self.buttons = []
            
            # Xóa các nút ở trạng thái đích
            for button in self.goal_buttons:
                button.destroy()
            self.goal_buttons = []
            
            # Tạo trạng thái ban đầu ngẫu nhiên có thể giải
            numbers = list(range(1, N*N)) + [0]  # Tạo danh sách [1, 2, ..., N*N-1, 0]
            while True:
                random.shuffle(numbers)
                if is_solvable(numbers, N):
                    break
            blank_pos = numbers.index(0)  # Vị trí của ô trống
            
            self.current_state = NPuzzleState(numbers, blank_pos)
            
            # Tạo nút cho từng ô của bảng
            for i in range(N):
                for j in range(N):
                    idx = i * N + j
                    btn = ttk.Button(self.puzzle_frame, text=str(numbers[idx]) if numbers[idx] != 0 else "",
                                   width=5)
                    btn.grid(row=i, column=j, padx=2, pady=2)
                    self.buttons.append(btn)
            
            # Tạo nút cho trạng thái đích
            goal_numbers = list(range(1, N*N)) + [0]  # Trạng thái đích [1, 2, ..., N*N-1, 0]
            for i in range(N):
                for j in range(N):
                    idx = i * N + j
                    btn = ttk.Button(self.goal_frame, text=str(goal_numbers[idx]) if goal_numbers[idx] != 0 else "",
                                   width=5, state="disabled")
                    btn.grid(row=i, column=j, padx=2, pady=2)
                    self.goal_buttons.append(btn)
                    
        except ValueError as e:
            messagebox.showerror("Error", str(e))  # Hiển thị lỗi nếu nhập không hợp lệ

    # Hàm giải câu đố
    def solve_puzzle(self):
        if not self.current_state:
            messagebox.showerror("Error", "Generate a puzzle first!")  # Cảnh báo nếu chưa tạo bảng
            return
            
        N = int(self.n_var.get())
        solution = dfs(self.current_state, N)  # Tìm giải pháp với hàm dfs
        
        if solution:
            messagebox.showinfo("Solution", " -> ".join(solution))  # Hiển thị chuỗi bước giải
            
            # Hiển thị quá trình giải bằng cách di chuyển các ô
            self.animate_solution(solution, 0)
        else:
            messagebox.showinfo("No Solution", "No solution found!")  # Thông báo nếu không tìm được giải pháp

    # Hàm hiển thị quá trình di chuyển các ô theo giải pháp
    def animate_solution(self, solution, move_index):
        if move_index >= len(solution):
            return
            
        N = int(self.n_var.get())
        valid_moves = get_valid_moves(self.current_state, N)  # Lấy các nước đi hợp lệ
        move_details = next((m for m in valid_moves if m[0] == solution[move_index]), None)
        
        if move_details:
            self.current_state = apply_move(self.current_state, move_details)  # Cập nhật trạng thái
            self.update_display()  # Cập nhật giao diện
            self.root.after(500, self.animate_solution, solution, move_index + 1)  # Lặp lại sau 500ms

    # Hàm cập nhật giao diện hiển thị trạng thái bảng hiện tại
    def update_display(self):
        N = int(self.n_var.get())
        total_cells = N * N
        
        # Đảm bảo không truy cập ngoài danh sách các nút
        for i in range(min(len(self.buttons), len(self.current_state.board))):
            value = self.current_state.board[i]
            self.buttons[i].configure(text=str(value) if value != 0 else "")

# Hàm kiểm tra xem bảng có thể giải được hay không
def is_solvable(board, N):
    inversions = 0
    for i in range(len(board)):
        for j in range(i + 1, len(board)):
            if board[i] != 0 and board[j] != 0 and board[i] > board[j]:
                inversions += 1
    
    # Với N lẻ: số đảo phải chẵn để có thể giải được
    # Với N chẵn: (hàng của ô trống từ dưới lên + số đảo) phải lẻ để giải được
    blank_row = board.index(0) // N
    if N % 2 == 1:
        return inversions % 2 == 0
    else:
        return (inversions + blank_row) % 2 == 1

# Hàm chính khởi tạo và chạy ứng dụng
def main():
    root = tk.Tk()
    app = NPuzzleGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
