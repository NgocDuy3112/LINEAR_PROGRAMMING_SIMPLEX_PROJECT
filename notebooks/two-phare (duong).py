import numpy as np
import os
class two_phase_simplex():

    '''Phương pháp 2 pha phương trình tuyến tính dạng CHUẨN'''

    def __init__(self):

        self.bang = None
        self.RHS = None
        self.ham_muc_tieu = None
        self.min_max = None
        self.dem_rangbuoc = None

    def ham_phuong_trinh(self):

        '''cắt từng phần tử của phương trình, rồi đưa vào các biến tạm thời'''

        try:
            self.min_max, self.dem_rangbuoc = input('\nNhập:\n\n').split()
        except ValueError:
            print('Dòng đầu tiên phải chứa hai giá trị')
            print('Chương trình kết thúc...')
            exit()

        if self.min_max not in ['MIN', 'MAX']:
            print ("Chỉ nhập MIN hoặc MAX ở dòng đầu tiên")
            print ("Chương trình kết thúc...")
            exit()

        try:
            self.dem_rangbuoc = int(self.dem_rangbuoc)
        except ValueError as e:
            print ("các số ràng buộc phải là số nguyên '{}'".format(dem_rangbuoc))
            print ('Chương trình kết thúc...')
            exit()

        phuong_trinh = list()
        RHS = list()

        # Lấy hàm mục tiêu
        eq = input().split()
        self.ham_muc_tieu = len(eq)
        phuong_trinh.append([int(i) for i in eq])

        # Lấy biến ràng buộc
        for i in list(range(self.dem_rangbuoc)):
            eq = input().split()
            if len(eq) != (self.ham_muc_tieu + 1):
                print( "nhập ràng buộc sai")
                print ("Chương trình kết thúc...")
                exit()
            try:
                RHS.append(int(eq[-1]))
                phuong_trinh.append([int(i) for i in eq[:-1]])
            except ValueError as e:
                print(e)
                print( "Chương trình kết thúc...")
                exit()

        # Đặt các biến bên RHS bằng 0 và đưa chúng vào phương trình
        RHS.append(0)
        phuong_trinh.append(phuong_trinh.pop(0))

        self.bang = phuong_trinh #Đưa phương trình vào bảng
        self.RHS = RHS #Đưa biến bên phải bằng 0 vào RHS

    def pprint(self, bang):

        '''Xuất kết quả của mỗi bảng'''

        print
        for i in bang:
            for j in i:
                print(str(round(j,2))+'\t',)
            print()
        print()

    def Ket_qua(self, diem_toi_uu):


        # đổi dấu giá trị của hàm mục tiêu nếu hàm mục tiêu là MAX
        gia_tri_toi_uu = self.bang[-1][-1] #Lấy giá trị tối ưu từ bảng
        if self.min_max == 'MAX':
            gia_tri_toi_uu *= -1.0

        # cập nhật điểm tối ưu
        diem = list()
        for i in [0,1]:
            if i in diem_toi_uu:
                diem.append(self.bang[diem_toi_uu.index(i)][-1])
            else:
                diem.append(0.0)

        return diem, gia_tri_toi_uu

    def dang_chuan(self):

        '''
        Chuyển bài toán sang dạng chuẩn bằng cách thêm biến phụ
        '''

        # Thêm biến phụ vào bảng
        for eq in self.bang:
            eq.extend([0]*self.dem_rangbuoc)
        for i, eq in enumerate(self.bang[:-1]):
            if self.RHS[i] < 0:
                eq[i+self.ham_muc_tieu] = -1
            else:
                eq[i+self.ham_muc_tieu] = 1

        # Chuyển bài toán từ cực tiểu sang cực đại bằng cách đổi dấu
        self.bang = np.array(self.bang, dtype=float)
        if self.min_max == 'MIN':
            self.bang[-1] = self.bang[-1]*-1 + 0.0

        self.RHS =  np.array(self.RHS)
        self.bang = np.hstack((self.bang, self.RHS[:,np.newaxis]))

    def them_bien(self):

        '''Tạo thêm các biến phụ nếu không có đủ các biến'''

        variable = True
        for i in list(range(self.ham_muc_tieu, self.ham_muc_tieu + self.dem_rangbuoc)):
            if np.sum(self.bang[:,i]) != 1:
                variable = False
                art_var = np.zeros((self.dem_rangbuoc + 1, 1))
                art_var[i-self.ham_muc_tieu] = 1.0
                self.bang = np.hstack((self.bang, art_var))
                self.bang[:,(-2,-1)] = self.bang[:,(-1,-2)]

        return variable

    def toi_uu(self):

        '''
        Tối ưu các ràng buộc của phare 1 và đưa vào bảng.
        Nếu có biến phụ thì đưa vào danh sách các biến phụ
        '''

        biem_temp = list()
        for i in list(range(self.ham_muc_tieu + self.dem_rangbuoc, self.bang.shape[1]-1)):
            row_id = np.where(self.bang[:,i]<0)[0]
            if list(row_id): 
                biem_temp.append(self.ham_muc_tieu + row_id[0])
                self.bang[-1][self.ham_muc_tieu + row_id[0]] = -1
                self.bang[-1] += self.bang[row_id[0]]

        return biem_temp

    def simplex(self,diem_toi_uu):




        self.pprint(self.bang)
        while not np.all(self.bang[-1][:-1] <= 0):
            pivot_col = np.argmax(self.bang[-1][:-1])
            # Kiểm tra các trường hợp không giới nội
            if np.all(self.bang[:,pivot_col][:-1] <= 0)  or \
                np.all(self.bang[:,-1][:-1] < 0):
                print ('Bai toan khong gioi noi')
                exit()
            theta = self.bang[:,-1][:-1] / self.bang[:,pivot_col][:-1]
	    # kiểm tra trường hợp theta âm
            if np.all(theta < 0):
                
                exit()
            # Đổi số âm thành 1 số lớn
            theta[self.bang[:,-1][:-1] < 0] = float('inf')
            theta[self.bang[:,pivot_col][:-1] < 0] = float('inf')
            # chọn hàng pivot và chuyển đổi các dòng với nhau bằng cách sử dụng  row operations
            pivot_row = np.argmin(theta)
            self.bang[pivot_row] /= self.bang[pivot_row][pivot_col]
            # đặt ma trận đơn vị bằng cách sử dụng row operations
            for i in list(range(self.dem_rangbuoc + 1)):
                if pivot_col > len(self.bang) or pivot_row > len(self.bang): #Nếu trường hợp số cột và số hàng lớn hơn sức chứa của bảng 
                    print ('Bai toan vo nghiem')
                    exit()
                else:
                    if i == pivot_row: continue
                    self.bang[i] = self.bang[i]-(self.bang[i][pivot_col]/ \
                        self.bang[pivot_row][pivot_col])* \
                        self.bang[pivot_row]
            self.pprint(self.bang)
            # cập nhật lại danh sách các biến cơ bản
            diem_toi_uu[pivot_row] = pivot_col

        return diem_toi_uu

    def two_phase(self):

        '''
        Kiểm tra xem nếu nó thuộc dạng bình thường b > 0 thì không cần sử dụng 2 pha, mà chuyển vào simplex
        còn nếu là các trường hợp đặc biệt thì sử dụng 2 pha. Tạo các biến phụ và thêm vào bảng sau đó chạy phare 1
        Nếu phare 1 chạy thành công và không rơi vào trường hợp không giới nội hay vô nghiệm thì chạy pha 2 bằng cách sử dụng simplex
        '''

        # lưu lại bảng gốc
        Z = self.bang[-1]
        bfs = self.them_bien() # thêm biến phụ ví dụ W1 W2 W3

        # tạo danh sách các biến cơ bản
        init_opt_pt = list(range(self.ham_muc_tieu,self.ham_muc_tieu + self.dem_rangbuoc))

        # nếu có biến phụ tồn tại
        if bfs:
            print ("\nGiải....")
            diem_toi_uu = self.simplex(init_opt_pt)
            return self.Ket_qua(diem_toi_uu)

        # Nếu không có biến phụ ban đầu
        # nếu có RHS nào âm thì đổi sang dương
        neg_RHS = self.bang[:,-1] < 0
        self.bang[neg_RHS] = self.bang[neg_RHS] * -1.0 + 0.0

        # đặt lại hàm mục tiêu mới với các biến là 0
        self.bang[-1] = np.zeros(self.bang.shape[1])
        biem_temp = self.toi_uu()

        # pha 1
        print( "\nPha 1....")
        diem_toi_uu = self.simplex(init_opt_pt)

        # loại bỏ các biến và đặt lại biến hàm mục tiêu và trong bảng 
        self.bang = np.delete(self.bang, biem_temp, axis=1)
        self.bang[-1] = Z
        # Kiểm tra ma trận đơn vị
        for row, col in enumerate(diem_toi_uu):
            self.bang[-1] -= self.bang[-1][col] * self.bang[row]
        # Pha 2
        print ("\nPha 2....")
        diem_toi_uu = self.simplex(diem_toi_uu)

        return self.Ket_qua(diem_toi_uu)


if __name__ == '__main__':

    result = two_phase_simplex()

    # lấy phương trình rồi chuẩn hóa thành dạng chuẩn
    result.ham_phuong_trinh()
    result.dang_chuan()

    # call two-phase simplex method
    diem_toi_uu, gia_tri_toi_uu = result.two_phase()

    # print results
    print ('\nOutput:\n')
    print( 'Optimal point is {}'.format(diem_toi_uu))
    print ('Optimal value is {}'.format(gia_tri_toi_uu))
    os.system('cls')