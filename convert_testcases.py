import os
import shutil
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox

# fun chuyển đổi các file trong thư mục gốc sang định dạng mới trong thư mục đích
def convert_files(source_folder, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # lấy danh sách các folder con trong folder gốc
    test_folders = [f for f in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, f))]

    # duyệt các thư mục con và convert các file
    for idx, test_folder in enumerate(test_folders, start=1):
        test_folder_path = os.path.join(source_folder, test_folder)
        new_folder_name = f"{os.path.basename(source_folder)}_QDUOJ"
        new_folder_path = os.path.join(target_folder, new_folder_name)
        if not os.path.exists(new_folder_path):
            os.makedirs(new_folder_path)

        for file_name in os.listdir(test_folder_path):
            if file_name.endswith(".inp"):
                new_file_name = f"{idx}.in"
            elif file_name.endswith(".out"):
                new_file_name = f"{idx}.out"
            else:
                continue

            source_file = os.path.join(test_folder_path, file_name)
            target_file = os.path.join(new_folder_path, new_file_name)
            shutil.copy2(source_file, target_file)

# fun chuyển đổi các file thành định dạng cụ thể cho HackerRank
def convert_files_hackerrank(source_folder, target_folder):
    source_folder_name = os.path.basename(source_folder)
    hackerrank_folder = os.path.join(target_folder, f"{source_folder_name}_HackerRank")
    if not os.path.exists(hackerrank_folder):
        os.makedirs(hackerrank_folder)

    # tạo các thư mục input và output trong thư mục đích
    input_folder = os.path.join(hackerrank_folder, "input")
    output_folder = os.path.join(hackerrank_folder, "output")
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)

    # lấy danh sách các folder con trong folder gốc
    test_folders = [f for f in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, f))]

    # duyệt các thư mục con và convert các file
    for idx, test_folder in enumerate(test_folders, start=1):
        test_folder_path = os.path.join(source_folder, test_folder)

        for file_name in os.listdir(test_folder_path):
            if file_name.endswith(".inp"):
                new_file_name = f"test{idx:02d}.inp"
                target_file = os.path.join(input_folder, new_file_name)
            elif file_name.endswith(".out"):
                new_file_name = f"test{idx:02d}.out"
                target_file = os.path.join(output_folder, new_file_name)
            else:
                continue

            source_file = os.path.join(test_folder_path, file_name)
            shutil.copy2(source_file, target_file)

# fun mở hộp chọn thư mục và cập nhật nhãn
def select_folder(label, is_source=True):
    folder = filedialog.askdirectory(title="Chọn thư mục", mustexist=True)
    if folder:
        label.config(text=f"{'Thư mục gốc' if is_source else 'Thư mục đích'}: {folder}")
        return folder
    return None

# fun xử lý chuyển đổi QDUOJ khi nhấn nút
def convert_qduoj():
    if source_folder.get() and target_folder.get():
        convert_files(source_folder.get(), target_folder.get())
        qduoj_status_label.config(text="Chuyển đổi QDUOJ hoàn tất!", fg="green", font=("Helvetica", 10, "bold"))
    else:
        messagebox.showerror("Lỗi", "Vui lòng chọn cả thư mục gốc và thư mục đích.")

# fun xử lý chuyển đổi HackerRank khi nhấn nút
def convert_hackerrank():
    if source_folder_hackerrank.get() and target_folder_hackerrank.get():
        convert_files_hackerrank(source_folder_hackerrank.get(), target_folder_hackerrank.get())
        hackerrank_status_label.config(text="Chuyển đổi HackerRank hoàn tất!", fg="green", font=("Helvetica", 10, "bold"))
    else:
        messagebox.showerror("Lỗi", "Vui lòng chọn cả thư mục gốc và thư mục đích.")

# fun nén thư mục thành file ZIP
def convert_to_zip():
    if not source_folder_zip.get() or not destination_folder_zip.get():
        messagebox.showerror("Lỗi", "Vui lòng chọn cả thư mục gốc và thư mục đích.")
        return

    source_folder_name = os.path.basename(source_folder_zip.get())
    zip_file_name = f"{source_folder_name}.zip"
    zip_file_path = os.path.join(destination_folder_zip.get(), zip_file_name)

    # tạo file ZIP và thêm các file vào
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(source_folder_zip.get()):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, source_folder_zip.get()))

    zip_status_label.config(text=f"Thư mục đã được nén thành {zip_file_path}", fg="green", font=("Helvetica", 10, "bold"))

root = tk.Tk()
root.title("Chuyển đổi File")
root.geometry("600x500")

# biến chứa đường dẫn thư mục
source_folder = tk.StringVar()
target_folder = tk.StringVar()
source_folder_zip = tk.StringVar()
destination_folder_zip = tk.StringVar()
source_folder_hackerrank = tk.StringVar()
target_folder_hackerrank = tk.StringVar()

# tạo khung chính và các khung con cho từng chức năng
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10, fill="both", expand="yes")

# frame chuyển QDUOJ
qduoj_frame = tk.LabelFrame(main_frame, text="Chuyển đổi QDUOJ", padx=10, pady=10)
qduoj_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

source_label = tk.Label(qduoj_frame, text="Chưa chọn thư mục gốc")
source_label.pack(pady=5)

target_label = tk.Label(qduoj_frame, text="Chưa chọn thư mục đích")
target_label.pack(pady=5)

btn_select_source = tk.Button(qduoj_frame, text="Chọn thư mục gốc",
                              command=lambda: source_folder.set(select_folder(source_label)))
btn_select_source.pack(pady=5)

btn_select_target = tk.Button(qduoj_frame, text="Chọn thư mục đích",
                              command=lambda: target_folder.set(select_folder(target_label, False)))
btn_select_target.pack(pady=5)

btn_convert_qduoj = tk.Button(qduoj_frame, text="Chuyển đổi QDUOJ", command=convert_qduoj)
btn_convert_qduoj.pack(pady=10)

qduoj_status_label = tk.Label(qduoj_frame, text="", fg="red")
qduoj_status_label.pack(pady=5)

# frame chuyển HackerRank
hackerrank_frame = tk.LabelFrame(main_frame, text="Chuyển đổi HackerRank", padx=10, pady=10)
hackerrank_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")

source_label_hackerrank = tk.Label(hackerrank_frame, text="Chưa chọn thư mục gốc")
source_label_hackerrank.pack(pady=5)

target_label_hackerrank = tk.Label(hackerrank_frame, text="Chưa chọn thư mục đích")
target_label_hackerrank.pack(pady=5)

btn_select_source_hackerrank = tk.Button(hackerrank_frame, text="Chọn thư mục gốc",
                                         command=lambda: source_folder_hackerrank.set(
                                             select_folder(source_label_hackerrank)))
btn_select_source_hackerrank.pack(pady=5)

btn_select_target_hackerrank = tk.Button(hackerrank_frame, text="Chọn thư mục đích",
                                         command=lambda: target_folder_hackerrank.set(
                                             select_folder(target_label_hackerrank, False)))
btn_select_target_hackerrank.pack(pady=5)

btn_convert_hackerrank = tk.Button(hackerrank_frame, text="Chuyển đổi HackerRank", command=convert_hackerrank)
btn_convert_hackerrank.pack(pady=10)

hackerrank_status_label = tk.Label(hackerrank_frame, text="", fg="red")
hackerrank_status_label.pack(pady=5)

# frame ZIP
zip_frame = tk.LabelFrame(main_frame, text="Chuyển đổi thành ZIP", padx=10, pady=10)
zip_frame.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

source_label_zip = tk.Label(zip_frame, text="Chưa chọn thư mục gốc")
source_label_zip.pack(pady=5)

destination_label_zip = tk.Label(zip_frame, text="Chưa chọn thư mục đích")
destination_label_zip.pack(pady=5)

btn_select_source_zip = tk.Button(zip_frame, text="Chọn thư mục gốc",
                                  command=lambda: source_folder_zip.set(select_folder(source_label_zip)))
btn_select_source_zip.pack(pady=5)

btn_select_destination = tk.Button(zip_frame, text="Chọn thư mục đích",
                                   command=lambda: destination_folder_zip.set(
                                       select_folder(destination_label_zip, False)))
btn_select_destination.pack(pady=5)

btn_convert_zip = tk.Button(zip_frame, text="Chuyển đổi thành ZIP", command=convert_to_zip)
btn_convert_zip.pack(pady=10)

zip_status_label = tk.Label(zip_frame, text="", fg="red")
zip_status_label.pack(pady=5)

# kích thước các cột của khung chính
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=1)
main_frame.columnconfigure(2, weight=1)

root.mainloop()
