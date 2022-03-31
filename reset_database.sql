

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

CREATE TABLE SoAccountDaLam
(
	soacc TINYINT
)

insert into SoAccountDaLam VALUEs (0)

SELECT soacc FROM SoAccountDaLam

UPDATE SoAccountDaLam SET soacc = 0
-- SELECT  fb_id, loai_job, link_fb,noi_dung_comment, [status] FROM BANGJOBS WHERE [status] = 0

-- UPDATE BANGJOBS SET status=1 WHERE fb_id = '100076681864851' AND loai_job = N'TĂNG LIKE CHO BÀI VIẾT' AND link_fb = 'https://www.facebook.com/325375386360597'

DELETE FROM BANGJOBS

