# Streamlit a docker workshop

> Autorem je Marek Šajner

Na tomto workshopu pro hackiton 2023 bude představen docker a streamlit.

Za normálních okolností je webový server(backend) oddělený od prezentační vrstvy(frontend), ale vy budete mít pouze 24 hodin na sestrojení celé webové aplikace. Pro toto se mimo jiné velmi hodí knihovna streamlit, která dokáže obojí. Navíc má přehledné API, a není potřeba používat javascript, HTML a CSS.

Abychom se vyhli nutnosti složitě konfigurovat služby, na což při hackatonu nebude čas, lze pro ně připravit předpis předem skrze Docker a pak je spouštět v izolovaném prostředí, kde nemohou nastávat konflikty mezi balíčky a nezahlcuje se jimi souborový systém PC.

Nejdříve promluvíme o základech streamlitu, poté zkusíme spustit nějaké služby skrze docker, dám vám pár doporučení(awesome docker, jupyter) a následně budou předvedeny složitější aplikace ve streamlitu. Když zbyde čas, popovídáme si o gitu, který je pro vícečlenné týmy naprostou nutností.

## Instalace

`./make_env.sh` pro úvodní instalaci.

Pak `docker-compose up --build` pro spuštění aplikací v dockerech. Aplikace většinu změn samy načtou, aniž by se compose musel restartovat. Vypíná se s Ctrl+C.

Na tomto workshopu používám linux, ale na windowsech to všechno taky půjde(je třeba přepsat zmíněný shell script)

Zvažte změnit hodnoty ve složce `./secrets`.

