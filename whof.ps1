
if (!(Test-Path Variable:PSScriptRoot)) {
 $PSScriptRoot = Split-Path $MyInvocation.MyCommand.Path -Parent 
}

$path = join-path "$env:chobanTools" "{packageExecutable}"


if($myinvocation.expectingInput) { $input | & $path  @args } else { & $path  @args }
