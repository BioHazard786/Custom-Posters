from mal import Anime

anime = Anime(32281)

if anime.type:
    if anime.type == "Movie":
        subtitle = f"""Movie{f' • {anime.aired.split(",")[-1].strip()}' if anime.aired else ''} • {anime.duration}"""
    else:
        subtitle = f"{f'{anime.premiered} • ' if anime.premiered else ''}{f'{anime.episodes} Episodes' if anime.episodes else anime.type or "Anime"}"
else:
    subtitle = f"{f'{anime.premiered} • ' if anime.premiered else ''}{f'{anime.episodes} Episodes' if anime.episodes else anime.type or "Anime"}"

print(subtitle)
