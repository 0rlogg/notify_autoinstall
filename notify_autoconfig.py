import os
import subprocess
import yaml

def check_go_version():
    try:
        version_output = subprocess.check_output(["go", "version"], text=True).strip()
        version = version_output.split(" ")[2][2:]
        return version
    except FileNotFoundError:
        print("Go no está instalado. Por favor, instálalo primero.")
        return None
    except Exception as e:
        print(f"Error al verificar la versión de Go: {e}")
        return None

def install_notify(go_version):
    try:
        if go_version >= "1.21":
            subprocess.run(["go", "install", "-v", "github.com/projectdiscovery/notify/cmd/notify@latest"], check=True)
        else:
            subprocess.run(["go", "install", "-v", "github.com/projectdiscovery/notify/cmd/notify@v1.0.6"], check=True)
        print("Notify instalado correctamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar Notify: {e}")
        exit(1)

def configure_notify():
    config_path = os.path.expanduser("~/.config/notify")
    os.makedirs(config_path, exist_ok=True)

    webhook = input("Introduce tu Discord Webhook URL: ")

    config_data = {
        "discord": [
            {
                "id": "crawl",
                "discord_channel": "crawl",
                "discord_username": "test",
                "discord_format": "{{data}}",
                "discord_webhook_url": webhook
            }
        ]
    }

    config_file = os.path.join(config_path, "provider-config.yaml")
    with open(config_file, "w") as file:
        yaml.dump(config_data, file, default_flow_style=False)
    
    print(f"Archivo de configuración creado en {config_file}")

def notify_path():
    notify_bin = os.path.expanduser("~/go/bin")
    current_path = os.getenv("PATH")

    if notify_bin not in current_path:
        with open(os.path.expanduser("~/.bashrc"), "a") as bashrc:
            bashrc.write(f'\nexport PATH="{notify_bin}:$PATH"\n')
        print("Notify añadido al PATH. Recuerda ejecutar `source ~/.bashrc` en tu terminal para recargar el PATH.")
    else:
        print("Notify ya está en el PATH.")

def notify_test():
    notify_path = os.path.expanduser("~/go/bin/notify")
    try:
        print("Probando Notify...")
        # Verificar si notify está en PATH, sino usar ruta completa
        result = subprocess.run(
            ["bash", "-c", f'echo "Hello world" | {notify_path} -silent'],
            text=True,
            capture_output=True
        )
        if result.returncode == 0:
            print(f"Prueba exitosa: {result.stdout.strip()}")
            print("Recuerda ejecutar `source ~/.bashrc` en tu terminal para recargar el PATH.")

        else:
            print(f"Prueba fallida: {result.stderr.strip()}")
    except Exception as e:
        print(f"Error al probar Notify: {e}")

def main():
    print("Verificando la versión de Go")
    go_version = check_go_version()

    if not go_version:
        return

    print(f"Versión de Go detectada: {go_version}")
    print("Instalando Notify...")
    install_notify(go_version)

    print("Configurando Notify...")
    configure_notify()

    print("Añadiendo Notify al PATH...")
    notify_path()

    print("Instalación y configuración completadas. Puedes usar Notify directamente desde tu terminal.")
    print("Para mas información consulta el repositorio de notify https://github.com/projectdiscovery/notify")

    # Realizar prueba de Notify
    notify_test()

if __name__ == "__main__":
    main()
