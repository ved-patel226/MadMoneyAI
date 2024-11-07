from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


def get_latest_video(
    playlist_url="https://www.youtube.com/playlist?list=PLVbP054jv0KoZTJ1dUe3igU7K-wUcQsCI",
):

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(playlist_url)

    try:
        latest_video = driver.find_element(
            By.XPATH, '//*[@id="contents"]/ytd-playlist-video-renderer[1]//a'
        )

        video_url = latest_video.get_attribute("href")

        return video_url
    except Exception as e:
        print("Error retrieving the latest video:", str(e))
        return None, None
    finally:
        driver.quit()


def main() -> None:
    video_url = get_latest_video()

    print("Latest video URL:", video_url)


if __name__ == "__main__":
    main()
