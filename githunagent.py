import subprocess
import os

# Uzantı listesi bu şekilde içine gömülebilir
uzanti_listesi = [
    "brunomnsilva.mingw-c-configuration",
    "christian-kohler.path-intellisense",
    "danielpinto8zz6.c-cpp-compile-run",
    "eamodio.gitlens",
    "ericsia.pythonsnippets3",
    "esbenp.prettier-vscode",
    "fougas.msys2",
    "franneck94.vscode-python-config",
    "github.codespaces",
    "github.copilot",
    "github.copilot-chat",
    "github.vscode-pull-request-github",
    "huangshao.console-manager",
    "irongeek.vscode-env",
    "kevinrose.vsc-python-indent",
    "local-rev.local-python-rev",
    "ms-azuretools.vscode-containers",
    "ms-ceintl.vscode-language-pack-tr",
    "ms-dotnettools.vscode-dotnet-runtime",
    "ms-python.debugpy",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.vscode-python-envs",
    "ms-vscode-remote.remote-wsl",
    "ms-vscode.cmake-tools",
    "ms-vscode.cpptools",
    "ms-vscode.cpptools-extension-pack",
    "ms-vscode.powershell",
    "nils-ballmann.python-coding-tools",
    "shd101wyy.markdown-preview-enhanced",
    "silasnevstad.gpthelper",
    "ted-996.python-editing-terminal",
    "wscats.delete-node-modules"
]

def yukle(extension_id):
    try:
        print(f"📦 Yükleniyor: {extension_id}")
        subprocess.run(f"code --install-extension {extension_id}", check=True, shell=True)
        print(f"✅ Yüklendi: {extension_id}\n")
    except subprocess.CalledProcessError:
        print(f"❌ Yüklenemedi: {extension_id}\n")

if __name__ == "__main__":
    for uzanti in uzanti_listesi:
        yukle(uzanti)
