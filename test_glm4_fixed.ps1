# 读取.env文件中的API密钥
$envFile = ".env"
if (Test-Path $envFile) {
    $envContent = Get-Content $envFile
    foreach ($line in $envContent) {
        if ($line -match 'GLM4_API_KEY=(.*)') {
            $apiKey = $matches[1]
            break
        }
    }
}

if (-not $apiKey) {
    Write-Host "请在.env文件中配置GLM-4-Flash API密钥" -ForegroundColor Red
    exit 1
}

# 构建测试提示
$prompt = "你好，请问你是谁？"

# 调用GLM-4-Flash API
$url = "https://open.bigmodel.cn/api/mt/chat/completions"
$headers = @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer $apiKey"
}
$data = @{
    "model" = "glm-4-flash"
    "messages" = @(
        @{
            "role" = "user"
            "content" = $prompt
        }
    )
    "temperature" = 0.7
} | ConvertTo-Json -Depth 3

Write-Host "正在测试GLM-4-Flash API..." -ForegroundColor Green

try {
    $response = Invoke-RestMethod -Uri $url -Method Post -Headers $headers -Body $data
    Write-Host "API调用成功!" -ForegroundColor Green
    Write-Host "\nAI回复:" -ForegroundColor Yellow
    Write-Host $response.choices[0].message.content
} catch {
    Write-Host "API调用失败: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.Exception.Response) {
        $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
        $responseBody = $reader.ReadToEnd()
        Write-Host "响应内容: $responseBody" -ForegroundColor Red
    }
}
