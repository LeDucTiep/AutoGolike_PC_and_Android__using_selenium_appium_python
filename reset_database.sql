

USE master
GO

DROP DATABASE jobsgolike
GO

CREATE DATABASE jobsgolike
GO

USE jobsgolike
GO

CREATE TABLE BANGJOBS
(
	STT INT IDENTITY(1,1) PRIMARY KEY,
	fb_id CHAR(15),
	loai_job NVARCHAR(50),
	link_fb NVARCHAR (100),
	noi_dung_comment NVARCHAR (200),
	status TINYINT
);



SELECT *
FROM BANGJOBS

-- CREATE TABLE SoAccountDaLam
-- (
-- 	soacc TINYINT
-- )
-- drop TABLE SoAccountDaLam
-- INSERT INTO SoAccountDaLam
-- VALUES
-- 	(0)

-- SELECT soacc
-- FROM SoAccountDaLam

-- UPDATE SoAccountDaLam SET soacc = 0

-- SELECT  fb_id, loai_job, link_fb,noi_dung_comment, [status] FROM BANGJOBS WHERE [status] = 0

-- UPDATE BANGJOBS SET status=1 WHERE fb_id = '100076681864851' AND loai_job = N'TĂNG LIKE CHO BÀI VIẾT' AND link_fb = 'https://www.facebook.com/325375386360597'

DELETE FROM BANGJOBS


-- tạo bảng tài khoản 
DROP TABLE taikhoan
CREATE TABLE taikhoan
(
	dang_lam INT DEFAULT (0),
	id_fb CHAR(15) PRIMARY KEY,
	ngay_lam_xong DATE DEFAULT '03-30-2022'
)
delete from taikhoan
INSERT INTO taikhoan
	(id_fb)
VALUES
	('100080122143986'),
	('100079883326930'),
	('100076681864851'),
	('100076630237844'),
	('100076621927821'),
	('100076609088552'),
	('100076487174292'),
	('100076469834611'),
	('100076469265711'),
	('100012962526153')

UPDATE taikhoan set dang_lam = 0
SELECT *
FROM taikhoan  where day(getdate()) != day(ngay_lam_xong)


delete taikhoan where id_fb = '100076379839853'
SELECT top(1)
	id_fb
FROM taikhoan
WHERE dang_lam = (SELECT min(dang_lam)
	FROM taikhoan where day(getdate()) != day(ngay_lam_xong))
and day(getdate()) != day(ngay_lam_xong)

UPDATE taikhoan 
SET dang_lam += 1
WHERE id_fb = "+id+"


UPDATE taikhoan 
SET ngay_lam_xong = GETDATE()
where id_fb = 






