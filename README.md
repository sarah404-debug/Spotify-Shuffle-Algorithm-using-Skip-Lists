# 🎵 Smart Shuffle Music Player (Skip List Based)

## 📌 Overview

This project is a **Smart Shuffle Music Player** built using **Python, Pygame, and Skip Lists**.
Unlike traditional shuffle systems that rely purely on randomness, this player uses **data structures** to create a **controlled, non-repetitive, and adaptive shuffle experience**.

The system ensures:

* No song repeats until all songs are played
* Efficient insertion, deletion, and search using skip lists
* A visually interactive GUI for playback

---

## 🚀 Features

* 🎶 **Smart Shuffle Algorithm**

  * Uses **two skip lists**:

    * Current playlist (songs yet to be played)
    * New playlist (already played songs)
  * Songs are played, deleted, and reinserted to ensure a full shuffle cycle

* ⚡ **Efficient Data Structure**

  * Skip Lists provide:

    * O(log n) insertion
    * O(log n) deletion
    * Fast traversal

* 🖥️ **Graphical User Interface (GUI)**

  * Built using **Pygame**
  * Displays:

    * Song list (left panel)
    * Currently playing song (right panel)
  * Includes:

    * “Next” button
    * Scrollable playlist
    * Gradient background

* 🔁 **No Repeat Guarantee**

  * Each song plays exactly once before reshuffling

---

## 🧠 Data Structures Used

### Skip List

A probabilistic data structure that allows fast search, insertion, and deletion.

Each node contains:

* Song data (title, artist, file path)
* Multiple forward pointers (levels)

---

## ⚙️ How It Works

1. All songs are inserted into the current skip list
2. When a song plays:

   * It is deleted from the current list
   * It is inserted into the new list
3. Once all songs are played:

   * The lists are swapped
   * Playback continues with a new shuffled structure

---

## 📂 Project Structure

```
SpotifyShuffle.py   # Main program  
songs.py            # Song dataset  
music/              # Folder containing MP3 files  
README.md           # Project documentation  
```

---

## ▶️ How to Run

### 1. Install Dependencies

```
pip install pygame
```

### 2. Run the Program

```
python SpotifyShuffle.py
```

---

## ⚠️ Important Notes

* Use forward slashes in file paths:

```
music/song_name.mp3
```

* Avoid using emojis in print statements on Windows (encoding issue)

---

## 📊 Time Complexity

| Operation      | Complexity |
| -------------- | ---------- |
| Insert         | O(log n)   |
| Delete         | O(log n)   |
| Search         | O(log n)   |
| Play Next Song | O(log n)   |

---

## 👥 Team Members

* Sarah
* Zainab
* Myrah

---

## 💡 Future Improvements

* True randomness using weighted selection
* Playlist filtering (genre, artist)
* Pause / Resume functionality
* Song progress bar
* Volume control

---

## 🎯 Conclusion

This project demonstrates how **Skip Lists** can be applied to build a real-world application.
It combines **data structures, algorithms, GUI, and audio processing** to create an interactive music player.

