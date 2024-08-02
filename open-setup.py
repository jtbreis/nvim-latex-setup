import iterm2
import os

async def main(connection):
    

    session_directory = os.path.expanduser("~/master-thesis/master-thesis")
    os.chdir(session_directory)

    app = await iterm2.async_get_app(connection)
    current_window = app.current_terminal_window

    tabs = []

    if current_window is not None:
        pdf_viewer_tab = await current_window.async_create_tab()
        pdf_viewer = pdf_viewer_tab.current_session
        commands = f"cd {session_directory} && zathura main.pdf\n"
        await pdf_viewer.async_send_text(commands)

        latex_compiler_tab = await current_window.async_create_tab()
        latex_compiler = latex_compiler_tab.current_session
        commands = f"cd {session_directory} && latexmk -pdf -pvc main.tex\n"
        await latex_compiler.async_send_text(commands)

        nvim_tab = await current_window.async_create_tab()
        nvim = nvim_tab.current_session
        commands = f"cd {session_directory} && nvim . \n"
        await nvim.async_send_text(commands)

        tabs.append(nvim_tab)
        tabs.append(latex_compiler_tab)
        tabs.append(pdf_viewer_tab)
    else:
        print("No current window found")

    await current_window.async_set_fullscreen(True)
    await current_window.async_set_tabs(tabs)


iterm2.run_until_complete(main)


