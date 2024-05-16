# DoBackupNow


# Sistema de Backup em Python usando 7zip

Este projeto implementa um sistema de backup utilizando o 7zip para arquivamento e compressão de arquivos. O sistema permite a realização de backups incrementais, detectando e arquivando apenas os arquivos modificados desde o último backup.

## Características

- **Backup Incremental:** Realiza o backup apenas dos arquivos modificados desde o último backup, economizando espaço e tempo.
- **Configuração via JSON:** Permite a configuração dos diretórios de origem e destino através de um arquivo JSON.
- **Log de Operações:** Mantém um log de todas as operações de backup para facilitar o rastreamento e a depuração.
- **Utilização do 7zip:** Usa o 7zip para compressão, garantindo uma compressão eficiente e suporte a múltiplos formatos de arquivo.

## Dependências

- Python 3.6 ou superior
- [7-Zip](https://www.7-zip.org/) instalado e acessível no PATH do sistema operacional

## Configuração

### Arquivo de Configuração (config.json)

Este arquivo contém as configurações dos grupos de backup, especificando os diretórios de origem e o destino dos backups. Exemplo:

```json
{
  "backup_groups": [
    {
      "source_directories": ["C:/path/to/documents", "D:/other/documents"],
      "backup_destination": "E:/backups"
    },
    {
      "source_directories": ["C:/another/path"],
      "backup_destination": "F:/backup_folder"
    }
  ]
}
```

### Caminho do 7-Zip

O caminho para o executável do 7-Zip deve ser configurado na constante `SEVEN_ZIP_PATH` no script Python:

```python
SEVEN_ZIP_PATH = r"C:/Program Files/7-Zip/7z.exe"
```

## Utilização

1. Modifique o arquivo `config.json` conforme necessário, adicionando os diretórios de origem e o destino dos backups.
2. Execute o script Python para iniciar o processo de backup:

   ```bash
   python DoBackupNow.py
   ```

## Estrutura do Projeto

- `DoBackupNow.py`: Script principal que executa os backups conforme as configurações.
- `config.json`: Arquivo de configuração que define os grupos de backup.
- `backup.log`: Log das operações de backup, gerado pelo script.

## Autor

- Francisco Barboza

## Histórico de Versões

- **1.0.0** - Implementação inicial do backup.
- **1.0.1** - Adicionada a funcionalidade de backup incremental.

## Licença

Este projeto é distribuído sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
