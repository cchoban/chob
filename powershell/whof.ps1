
if (!(Test-Path Variable:PSScriptRoot)) {
 $PSScriptRoot = Split-Path $MyInvocation.MyCommand.Path -Parent
}

$path = join-path "$env:chobanApps" "{packageExecutable}"


if($myinvocation.expectingInput) { $input | & $path  @args } else { & $path  @args }
