@echo off

for %%f in (%*) do (
  "%~dp0\build\phonetic.exe" %%f
)

pause