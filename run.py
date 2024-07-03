from pytube import YouTube
from pydub import AudioSegment
import os

def youtube_to_wav(url, output_path):
    try:
        # YouTube 객체 생성
        yt = YouTube(url)
        
        # 영상 제목 가져오기 및 파일 이름으로 사용 가능하게 처리
        video_title = yt.title
        safe_title = "".join([c for c in video_title if c.isalnum() or c in (' ', '-', '_')]).rstrip()
        
        # 오디오 스트림 추출
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        # output 폴더 생성 (없는 경우)
        os.makedirs(output_path, exist_ok=True)
        
        # 임시 파일로 다운로드
        temp_file = audio_stream.download(output_path=output_path, filename="temp")
        
        # 파일 이름 변경 (영상 제목 사용)
        base, ext = os.path.splitext(temp_file)
        new_file = os.path.join(output_path, safe_title + '.mp4')
        os.rename(temp_file, new_file)
        
        # MP4를 WAV로 변환
        audio = AudioSegment.from_file(new_file, format="mp4")
        wav_file = os.path.join(output_path, safe_title + '.wav')
        audio.export(wav_file, format="wav")
        
        # 임시 MP4 파일 삭제
        os.remove(new_file)
        
        print(f"WAV 파일이 성공적으로 저장되었습니다: {wav_file}")
    except Exception as e:
        print(f"오류 발생: {str(e)}")

# 사용 예시
url = input("변환하고 싶은 YouTube 영상 URL을 입력하세요: ")
output_path = "output"  # output 폴더에 저장

youtube_to_wav(url, output_path)
