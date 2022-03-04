mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"j.pastor18@ejm.org\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
