import dash

external_script = ["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]
app = dash.Dash(
    __name__,
    external_scripts=external_script,
    use_pages=True, 
    pages_folder="/home/python/app/code/core/pages",
    suppress_callback_exceptions=True
)
app.scripts.config.serve_locally = True


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
 