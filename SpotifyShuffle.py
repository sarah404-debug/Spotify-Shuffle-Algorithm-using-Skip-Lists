# TEAM MEMBERS: SARAH, ZAINAB, MYRAH

# Smart Shuffle Music Player: Uses two skip lists to manage a playlist of 28 songs.
# Plays a song, deletes it from the current skip list, adds it to a new skip list.
# After all 28 songs are played, swaps to the new skip list for random order playback.
# GUI shows song list (left) and current song (right).

import random
# Provides random number generation for assigning node heights in the skip list.
import pygame #Imports the pygame library for multimedia applications.
# Handles audio playback (MP3s) and GUI (window, text, input).
import asyncio #Imports the asyncio module, which supports asynchronous programming (running tasks that can pause and resume).
# Ensures non-blocking GUI in Pyodide (browser-based Python).
import platform #Imports the platform module, which provides information about the system the code is running on.
# Checks if running in Pyodide (Emscripten) to run main() asynchronously.
from songs import SONGS
# Imports the SONGS list containing 30 songs, each with title, artist, file_path.

# Initialize pygame
pygame.init() #Initializes all Pygame modules (graphics, sound, input).
# Prepares Pygame for creating the window and playing music.
pygame.mixer.init() #Initializes Pygame’s audio mixer for playing MP3s.
# Sets up the audio system to load and play song files.

# Constants
MAX_HEIGHT = 6 #for 30 songs 5 would suffice as log_2(28) ≈ 4.8 so 5, +1 for buffer
# Maximum height of skip list nodes (levels 0 to 6) for efficient searching.
current_song_node = None
# Tracks the currently playing song’s node in the skip list.

#SARAH
# Initialize two skip lists
current_head = {"value": None, "next": [None] * (MAX_HEIGHT + 1)}
# Head of the current skip list, holds songs to be played, starts empty.
new_head = {"value": None, "next": [None] * (MAX_HEIGHT + 1)}
# Head of the new skip list, holds played songs, starts empty.
current_level = 0
# Highest level with nodes in the current skip list.
new_level = 0
# Highest level with nodes in the new skip list.
current_size = 0
# Number of songs in the current skip list.
new_size = 0
# Number of songs in the new skip list.

#MYRAH
# Create a node as a dictionary
def make_node(value, height):
    # Creates a skip list node with song data and links for given height.
    return {"value": value, "next": [None] * (height + 1)}
    # value: Song data (dictionary with title, artist, file_path).
    # next: List of pointers to next nodes at each level (0 to height).

#ZAINAB
# Pick random height
def pick_height():
    # Assigns a random height to a skip list node for randomization.
    h = 0
    # Starts at level 0 (all nodes have at least level 0).
    while random.randint(0, 1) and h < MAX_HEIGHT:
        # Flips a coin (0 or 1); if 1 and below MAX_HEIGHT, increase height.
        h += 1 #Builds the random height for the node.
    return h
    # Returns height (0 to MAX_HEIGHT), randomizing node placement.

#MYRAH
# Add a song to a skip list
def add(head, level, size, song_data):
    # Adds a song to the skip list, sorted by title, with random height.
    update = [None] * (MAX_HEIGHT + 1)
    # Stores nodes just before the insertion point at each level.
    current = head
    # Starts traversal from the head of the skip list.
    for r in reversed(range(level + 1)):
        # Loops from highest level down to 0 for efficient search.
        while current["next"][r] and current["next"][r]["value"] and current["next"][r]["value"]["title"] < song_data["title"]:
            # Moves forward if next node exists and its title is less than song’s.
            current = current["next"][r]
        update[r] = current
        # Saves the last node before the insertion point at this level.

    current = current["next"][0]
    # Checks level 0 to confirm if song already exists.
    if current and current["value"]["title"] == song_data["title"]:
        # If song exists, return without adding.
        return head, level, size, False

    h = pick_height()
    # Gets a random height for the new node.
    if h > level:
        # If new height exceeds current level, update level.
        for i in range(level + 1, h + 1):
            update[i] = head
            # Sets update nodes to head for new higher levels.
        level = h
        # Updates the skip list’s maximum level.

    new_node = make_node(song_data, h)
    # Creates a new node with song data and height.
    for i in range(h + 1):
        # Links the new node at each level up to its height.
        new_node["next"][i] = update[i]["next"][i]
        # Points new node to the next node.
        update[i]["next"][i] = new_node
        # Points previous node to new node.

    size += 1
    # Increments the skip list size.
    return head, level, size, True
    # Returns updated head, level, size, and success flag.

#ZAINAB
# Search for a song
def search(head, level, song_title):
    # Searches for a song by title in the skip list.
    current = head
    # Starts from the head node.
    for r in reversed(range(level + 1)):
        # Traverses from highest level down for efficiency.
        while current["next"][r] and current["next"][r]["value"] and current["next"][r]["value"]["title"] < song_title:
            # Moves forward if next node’s title is less than target.
            current = current["next"][r]
    current = current["next"][0]
    # Checks level 0 for the exact song.
    return current is not None and current["value"]["title"] == song_title
    # Returns True if song is found, False otherwise.

#ZAINAB AND SARAH
# Delete a song
def delete(head, level, size, value):
    # Deletes a song from the skip list by its song data (title match).
    update = [None] * (MAX_HEIGHT + 1)
    # Stores nodes just before the deletion point at each level.
    current = head
    # Starts traversal from the head.
    for r in reversed(range(level + 1)):
        # Loops from highest level down.
        while current["next"][r] and current["next"][r]["value"] and current["next"][r]["value"]["title"] < value["title"]:
            # Moves forward if next node’s title is less than target.
            current = current["next"][r]
        update[r] = current
        # Saves the node before the deletion point.

    current = current["next"][0]
    # Checks level 0 for the song to delete.
    if not current or current["value"]["title"] != value["title"]:
        # If song not found, print message and return.
        print(f"Song '{value['title']}' not found.")
        return head, level, size, False

    for i in range(len(current["next"])):
        # Updates pointers to skip the deleted node at each level.
        update[i]["next"][i] = current["next"][i]

    while level > 0 and head["next"][level] is None:
        # Reduces level if the highest level is now empty.
        level -= 1

    size -= 1
    # Decrements the skip list size.
    print(f"Song '{value['title']}' deleted.")
    return head, level, size, True
    # Returns updated head, level, size, and success flag.

#SARAH
# Play the first song at the highest level
def play_next_song():
    # Plays the first song at the highest level, deletes it, adds to new skip list.
    global current_song_node, current_head, current_level, current_size, new_head, new_level, new_size
    current = current_head["next"][0]
    # Checks if the current skip list has songs at level 0.
    if not current:
        # If empty, swap to new skip list.
        print("Current playlist empty. Changing to new playlist.")
        current_head, new_head = new_head, make_node(None, MAX_HEIGHT)
        # Swaps current and new skip lists, resets new skip list.
        current_level, new_level = new_level, 0
        # Updates levels.
        current_size, new_size = new_size, 0
        # Updates sizes.
        current = current_head["next"][0]
        # Checks the new current skip list.
        if not current:
            # If new skip list is empty, stop.
            print("No songs in new playlist.")
            current_song_node = None
            return

    # Find the first song at the highest non-empty level
    min_node = None
    # Will store the song to play.
    for level in reversed(range(current_level + 1)):
        # Checks levels from highest to lowest.
        if current_head["next"][level]:
            # If a song exists at this level, select it.
            min_node = current_head["next"][level]
            break
        # Breaks at the first non-empty level for randomization.

    if min_node is None:
        # If no song found, print error and stop.
        print("Error: No valid song found.")
        current_song_node = None
        return

    song_data = min_node["value"]
    # Gets the song’s data (title, artist, file_path).
    song_title = song_data["title"]
    # Extracts the song title.
    song_artist = song_data["artist"]
    # Extracts the artist name.
    file_path = song_data["file_path"]
    # Extracts the MP3 file path.

    print(f"\n Now Playing: {song_title} by {song_artist}")
    # Prints the song being played.
    current_song_node = min_node
    # Sets the current song node for GUI display.

    try:
        pygame.mixer.music.load(file_path)
        # Loads the MP3 file.
        pygame.mixer.music.play()
        # Plays the song.
        
        # Delete from current skip list
        current_head, current_level, current_size, success = delete(current_head, current_level, current_size, song_data)
        # Deletes the played song from the current skip list.
        
        # Add to new skip list
        if success:
            # If deletion succeeded, add song to new skip list.
            new_head, new_level, new_size, exists = add(new_head, new_level, new_size, song_data)
            # Adds song with random height for randomization.
    except Exception as e:
        # Handles errors in loading or playing the song.
        print(f"Error playing {song_title}: {e}")


#GUI MADE BY THE HELP OF AI ,THEN EDITED AND CHANGED BY US, MAIN PROGRAM WAS MADE BY ALL
# GUI and main program
async def main():
    # Main function: Sets up and runs the GUI, handles events, updates skip lists.
    global current_head, current_level, current_size, current_song_node
    # Accesses global skip list variables.
    # GUI setup
    WINDOW_WIDTH = 800 # Window width in pixels.
    WINDOW_HEIGHT = 600 # Window height in pixels.
    LIST_FONT_SIZE = 20 # Font size for song list (left panel).
    DETAIL_FONT_SIZE = 24 # Font size for current song details (right panel).
    BUTTON_WIDTH = 100 # Width of the "Next" button.
    BUTTON_HEIGHT = 40 # Height of the "Next" button.
    BLACK = (0, 0, 0) # Color: Black for text and lines.
    GRAY = (200, 200, 200) # Color: Gray for button background.
    BLUE = (0, 120, 255) # Color: Blue for song title text.
    FPS = 60 # Frames per second for smooth GUI updates.

    COLORS = [
        (250, 128, 114),
        (173, 216, 230),
        (144, 238, 144),
        (221, 160, 221),
    ]
    # List of colors for gradient background transition.
    current_color = COLORS[0] 
    target_color = COLORS[1]
    color_index = 1 # Index of next target color.
    transition_duration = 5.0 # Duration of color transition in seconds.
    transition_progress = 0.0 # Progress of color transition (0 to 1).

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Smart Shuffle Music Player")
    list_font = pygame.font.SysFont("Arial", LIST_FONT_SIZE)
    detail_font = pygame.font.SysFont("Arial", DETAIL_FONT_SIZE)
    clock = pygame.time.Clock()

    scroll_offset = 0
    song_height = LIST_FONT_SIZE + 4
    max_visible_songs = (WINDOW_HEIGHT - 50) // song_height # Number of songs visible in the left panel.

    # Initialize current skip list
    for song in SONGS: #adds songs to the skip list
        current_head, current_level, current_size, _ = add(current_head, current_level, current_size, song)
    play_next_song()
    # Plays the first song to start the player.

    next_button_rect = pygame.Rect(WINDOW_WIDTH - BUTTON_WIDTH - 10, WINDOW_HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT)

    running = True
    while running:
        transition_progress += 1.0 / (FPS * transition_duration) # Updates background color transition progress.
        if transition_progress >= 1.0: # If transition complete, switch to next color.
            transition_progress = 0.0
            current_color = target_color
            color_index = (color_index + 1) % len(COLORS)
            target_color = COLORS[color_index]
        r = int(current_color[0] + (target_color[0] - current_color[0]) * transition_progress)
        g = int(current_color[1] + (target_color[1] - current_color[1]) * transition_progress)
        b = int(current_color[2] + (target_color[2] - current_color[2]) * transition_progress)
        background_color = (r, g, b)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if next_button_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    play_next_song()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()
                    play_next_song()
            elif event.type == pygame.MOUSEWHEEL:
                scroll_offset -= event.y * song_height
                scroll_offset = max(0, min(scroll_offset, (current_size - max_visible_songs) * song_height))
    
        if current_song_node and not pygame.mixer.music.get_busy(): # If current song finished playing, play the next song.
            play_next_song()

        screen.fill(background_color)
        pygame.draw.line(screen, BLACK, (400, 0), (400, WINDOW_HEIGHT), 2) # Draws a vertical line to separate left and right panels.

       
        header_text = list_font.render("Song List", True, BLACK)
        screen.blit(header_text, (10, 10))
        y_offset = 50
        current = current_head["next"][0] # Starts at first song in current skip list.
        song_index = 0
        while current and current["value"]:
            # Loops through songs in the current skip list.
            if y_offset - scroll_offset >= 50 and y_offset - scroll_offset <= WINDOW_HEIGHT: # Only draws songs within the visible area.
                song_data = current["value"]
                title = song_data["title"]
                text_surface = list_font.render(title, True, BLACK)
                screen.blit(text_surface, (20, y_offset - scroll_offset)) # Draws song title with scroll adjustment.
            y_offset += song_height # Moves to next song position.
            current = current["next"][0] # Goes to next song.
            song_index += 1 # Increments song index.

        # Right panel: Current song
        if current_song_node:
            # If a song is playing, display its details.
            song_data = current_song_node["value"]
            title = song_data["title"]
            artist = song_data["artist"]
            now_playing_text = detail_font.render("Now Playing:", True, BLACK)
            title_text = detail_font.render(title, True, BLUE) # Renders song title in blue.
            artist_text = detail_font.render(f"by {artist}", True, BLACK)
            total_height = now_playing_text.get_height() + title_text.get_height() + artist_text.get_height() + 20 # Calculates total height of text for centering.
            y_start = (WINDOW_HEIGHT - total_height) // 2 # Centers text vertically.
            screen.blit(now_playing_text, (410, y_start)) # Draws "Now Playing".
            screen.blit(title_text, (410, y_start + now_playing_text.get_height() + 10)) # Draws song title.
            screen.blit(artist_text, (410, y_start + now_playing_text.get_height() + title_text.get_height() + 20)) # Draws artist name.

        pygame.draw.rect(screen, GRAY, next_button_rect) # Draws the "Next" button rectangle.
        button_text = detail_font.render("Next", True, BLACK) # Renders "Next" text.
        button_text_rect = button_text.get_rect(center=next_button_rect.center) # Centers text in button.
        screen.blit(button_text, button_text_rect) # Draws button text.

        pygame.display.flip() # Updates the window to show changes.
        clock.tick(FPS) # Limits loop to 60 FPS.
        await asyncio.sleep(1.0 / FPS) # Pauses briefly for non-blocking in Pyodide.

    pygame.mixer.music.stop() # Stops music when exiting.
    pygame.quit() # Closes Pygame and window.

if platform.system() == "Emscripten": # If running in Pyodide (browser), run main() asynchronously.
    asyncio.ensure_future(main())
else:
    # If running locally, run main() normally.
    if __name__ == "__main__":
        asyncio.run(main())