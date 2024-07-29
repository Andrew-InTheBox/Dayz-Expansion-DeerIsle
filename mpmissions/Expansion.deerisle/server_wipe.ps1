# Get the directory the script is being run from
$basePath = $PSScriptRoot

# Define the paths to remove
$pathsToRemove = @(
    "mpmissions\Expansion.chernarusplus\storage_1\*",
    "config\ExpansionMod\ATM\*",
    "config\ExpansionMod\AI\Spatial\SpatialPlayerSettings.json",
    "config\ExpansionMod\Quests\PersistentServerData.json",
    "config\ExpansionMod\Quests\GroupData\*",
    "config\ExpansionMod\Quests\PlayerData\*"
)

# Prompt for confirmation
$confirmation = Read-Host "Are you sure you want to delete the specified files? (yes/no)"

if ($confirmation -eq 'yes') {
    # Loop through each path and remove the files/directories
    foreach ($path in $pathsToRemove) {
        $fullPath = Join-Path -Path $basePath -ChildPath $path
        if (Test-Path $fullPath) {
            Remove-Item -Path $fullPath -Recurse -Force
            Write-Host "Removed: $fullPath"
        } else {
            Write-Host "Path not found: $fullPath"
        }
    }
    Write-Host "Server data wipe complete."
} else {
    Write-Host "Operation cancelled. No files were deleted."
}