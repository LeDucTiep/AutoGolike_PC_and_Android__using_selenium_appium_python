
# table: STT, fb_id, loai_job, link_fb, noi_dung_comment, status
# status:
# - 0: chưa làm 
# - 1: đã làm xong
# - 2: có lỗi

# gửi jobs lên 
# -> (fb_id, loai_job, link_fb, noi_dung_comment, status) values (fb_id, loai_job, link_fb, noi_dung_comment, 0)
# file: post_job.py

# - khi nào thì biết jobs đã làm xong mà còn báo cáo lấy xiền 
# -> mỗi 0.5 second lại kiểm tra status 1 lần
# file: get_status_request.py

# # lấy jobs về 
# select (fb_id, loai_job, link_fb, noi_dung_comment, status) from BANGJOBS 
# - làm xong jobs thì thông báo kiểu j cho client biết -> chỉnh status về 1 
# - giả sử có jobs lỗi thì thông báo ra sao -> chỉnh status về 2
# - nếu như không lỗi thì bao h xóa jobs đó đi (để lại sẽ làm cho database nặng, dữ liệu rác)
# -> Lấy job về. làm xong thì sửa status. lặp lại.
# file: get_job.py and post_status.py


# -> có vẻ như ta cần 1 anh tràng thứ 3 làm nhiệm vụ dọn rác (các jobs đã làm xong) 
# -* Vấn đề nghiêm trọng là làm cách nào để biết client đã nhận được thông tin jobs đó đã hoàn thành (đọc nó trước khi nó bị xóa)
# -> Trong thực tế 2 công việc này nên để 1 người làm. đọc xong thì xóa nó đi luân
# file: post_delete_job.py


# cần một bảng để lưu số tài khoản đã làm xong 

