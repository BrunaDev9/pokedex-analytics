# Pegar o diretório atual
$scriptDiretory = Split-Path -Path $myInvocation.MyCommand.Definition -Parent 


# Arquivo de saída com todos os SQL
$outputFile = Join-Path -Path $scriptDiretory -ChildPath "migration.sql"

# Verificar se o arquivo já existe, se existir deletar
if (Test-Path $outputFile) {
    Remove-Item $outputFile
}

# Pegar o conteúdo dos arquivos
$sqlFiles = Get-ChildItem -Path $scriptDiretory -Filter "*.sql" | Sort-Object Name

# Contatenar arquivos
foreach ($file in $sqlFiles) { 
 Get-Content $file.FullName | Out-File -Append -FilePath $outputFile "GO" | Out-File -Append -FilePath $outputFile  

}
Write-Host "Todos os arquivos SQL foram concatenados em $outputFile"
