# Azure 기반 기술 인터뷰 준비 가이드 (AWS 비교 + CLI 명령어 비교표)

## 1) 핵심 관점

Azure 면접을 AWS 경험 기준으로 준비할 때 가장 중요한 포인트는 다음 3가지입니다.

1. **서비스 이름 매핑**보다 **운영 모델 차이**를 설명할 수 있어야 한다.
2. **왜 그 서비스를 선택했는지**를 비교형으로 말할 수 있어야 한다.
3. **CLI / IaC / 보안 / 운영 자동화 경험**까지 연결해서 답할 수 있어야 한다.

예를 들어,

- "Azure VM은 AWS EC2와 비슷한 IaaS입니다."
- "AKS는 EKS와 비슷한 관리형 Kubernetes입니다."
- "Azure Functions는 Lambda와 유사한 서버리스 실행 환경입니다."
- "다만 Azure App Service와 AWS Elastic Beanstalk는 비슷해 보이지만 운영 체감은 꽤 다릅니다."

Azure CLI는 공식적으로 **cross-platform command-line tool for managing Azure resources**로 안내되며, `az login` 이후 활성 Subscription을 바꿔가며 작업할 수 있습니다. 또한 Azure PowerShell(`Az` 모듈)과 Azure Cloud Shell도 함께 제공됩니다. citeturn0search2turn0search6turn0search12turn0search10

---

## 2) Azure와 AWS 주요 서비스 매핑표

| Azure | AWS | 설명 |
|---|---|---|
| Tenant | Organization / 계정 조직 구조 | Azure의 상위 디렉터리/ID 관리 경계 |
| Subscription | AWS Account | 과금/권한/리소스 관리의 핵심 단위 |
| Resource Group | 완전 동일 서비스 없음 | 리소스를 논리적으로 묶어 관리하는 단위 |
| Virtual Machines | EC2 | 대표적인 IaaS 가상 서버 |
| App Service | Elastic Beanstalk(유사) | 웹앱/백엔드 배포용 PaaS 성격 |
| AKS | EKS | 관리형 Kubernetes |
| Azure Functions | Lambda | 서버리스 이벤트 실행 |
| VNet | VPC | 클라우드 가상 네트워크 |
| Subnet | Subnet | 네트워크 세분화 |
| NSG | Security Group 중심 비교 | 트래픽 제어 |
| Application Gateway | ALB | L7 로드밸런싱 |
| Front Door | CloudFront와 자주 비교 | 글로벌 진입점/가속/보안 |
| Blob Storage | S3 | 객체 스토리지 |
| Azure Files | EFS / FSx | 공유 파일 시스템 |
| Azure SQL Database | RDS | 관리형 관계형 DB |
| Cosmos DB | DynamoDB | NoSQL / 고확장성 |
| Key Vault | Secrets Manager + KMS | 비밀값/키/인증서 관리 |
| Azure RBAC | IAM | 권한 관리 |
| Managed Identity | IAM Role | 자격증명 없는 서비스 간 접근 |
| Azure Monitor / Log Analytics / App Insights | CloudWatch / X-Ray 일부 | 모니터링, 로그, APM |

---

## 3) 구조와 계정 개념 비교

### Azure
- **Tenant**: 조직/디렉터리 경계
- **Subscription**: 과금, 리소스, 권한 관리의 핵심 단위
- **Resource Group**: 관련 리소스를 묶는 논리 단위

### AWS
- **Organization**: 여러 계정을 조직적으로 관리
- **Account**: 과금/격리/권한의 핵심 단위
- **리소스 묶음 관리**: 태그, CloudFormation Stack, 프로젝트 단위 운영 등으로 보완

면접 답변 예시:

> "AWS에서 Account 단위로 dev/prod를 분리하듯, Azure에서는 Subscription으로 환경을 나누고 Resource Group으로 애플리케이션 묶음을 관리합니다."

Azure는 `az login` 후 기본 Subscription을 선택하고, `az account set --subscription ...`으로 활성 Subscription을 바꿀 수 있습니다. citeturn0search4turn0search6

---

## 4) 컴퓨팅 서비스 비교

### Azure VM ↔ AWS EC2
- 둘 다 운영체제와 패치, 런타임을 직접 관리하는 IaaS
- 커스터마이징은 좋지만 운영 부담이 큼

면접 포인트:
- 특정 OS 설정 필요
- 에이전트/보안 도구 직접 설치
- 레거시 앱 이전

### Azure App Service ↔ AWS Elastic Beanstalk
- 둘 다 웹 애플리케이션 배포에 사용
- **App Service가 더 강한 PaaS 느낌**
- **Elastic Beanstalk는 내부적으로 EC2, 로드밸런서, 오토스케일링 리소스가 더 직접적으로 드러남**

면접 답변 예시:

> "Azure App Service는 AWS Elastic Beanstalk와 유사하지만, App Service가 더 관리형 PaaS에 가깝다고 느꼈습니다. 운영체제나 인프라를 덜 신경 써도 돼서 API 서비스 운영에 적합했습니다."

### AKS ↔ EKS
- 둘 다 관리형 Kubernetes
- 컨테이너 표준화, 오토스케일링, Ingress, HPA, GitOps 등 확장성이 높음
- 대신 운영 난이도는 App Service나 Beanstalk보다 높음

### Azure Functions ↔ AWS Lambda
- 둘 다 서버리스
- 이벤트 기반 처리, 예약 작업, 경량 API 백엔드에 적합
- 짧고 독립적인 실행 단위에 유리

Azure Functions는 Azure의 이벤트 기반 서버리스 컴퓨트 서비스이고, AWS Lambda도 서버 관리 없이 코드를 실행하는 서버리스 서비스로 공식 문서에서 설명합니다. citeturn0search2turn0search13

---

## 5) 네트워크 비교

### VNet ↔ VPC
- 가장 대표적인 매핑
- 주소 대역, 서브넷, 라우팅, 보안 제어의 기본 단위

### Subnet ↔ Subnet
- 거의 동일 개념

### NSG ↔ Security Group 중심 비교
- Azure NSG는 서브넷/네트워크 인터페이스에 규칙 적용 가능
- AWS Security Group은 인스턴스/ENI 중심 가상 방화벽
- AWS NACL은 서브넷 단위 제어

면접 포인트:
- NSG는 SG와 가장 많이 비교하지만 구조는 완전히 같지 않음

### Application Gateway ↔ ALB
- HTTP/HTTPS L7 트래픽 처리
- 경로 기반 라우팅, SSL 종료 등과 자주 연결

### Front Door ↔ CloudFront 중심 비교
- 글로벌 진입점, 가속, 엣지 기반 배포, 웹 보안과 연결
- 정적 웹/글로벌 트래픽에서는 CloudFront와 비교 설명이 가장 자연스러움

AWS는 VPC를 가상 네트워크로 설명하고, CloudFront는 전역 엣지 배포 계층에서 자주 사용됩니다. Azure는 VNet과 Front Door로 대응해서 설명하는 것이 일반적입니다. citeturn0search2turn0search13

---

## 6) 스토리지 비교

### Blob Storage ↔ S3
- 가장 쉬운 매핑
- 정적 파일, 이미지, 문서, 로그, 백업, 미디어 저장

### Azure Files ↔ EFS / FSx
- 공유 파일 시스템 관점에서 비교
- 워크로드 특성에 따라 AWS 쪽은 EFS 또는 FSx로 나뉨

면접 답변 예시:

> "정적 자산이나 업로드 파일은 Azure Blob Storage를 썼고, AWS 기준으로 보면 S3와 거의 같은 역할로 설명할 수 있습니다."

---

## 7) 데이터베이스 비교

### Azure SQL Database ↔ AWS RDS
- 대표적인 관리형 관계형 DB 비교
- 백업, 고가용성, 운영 자동화를 서비스에 맡길 수 있음

### Cosmos DB ↔ DynamoDB
- NoSQL, 대규모 확장, 저지연 요구에 자주 비교
- 완전 동일하지는 않지만 면접에서는 가장 자연스러운 대응

면접 포인트:
- 트랜잭션 중심이면 Azure SQL / RDS
- 유연한 스키마, 대규모 읽기/쓰기, 전역 분산이면 Cosmos DB / DynamoDB 검토

AWS RDS는 관계형 DB를 손쉽게 설정, 운영, 확장할 수 있는 관리형 서비스로 공식 문서에서 설명됩니다. citeturn0search13

---

## 8) 보안과 비밀관리 비교

### Azure Key Vault ↔ AWS Secrets Manager + KMS
- Azure Key Vault는 비밀, 인증서, 키 관리 기능을 포괄적으로 제공
- AWS는 보통 비밀값은 Secrets Manager, 키 관리는 KMS로 나눠 설명

### Azure RBAC ↔ AWS IAM
- 둘 다 핵심 권한관리 체계
- Azure는 Subscription / Resource Group / Resource 계층 권한 모델 설명이 중요
- AWS는 IAM User / Role / Policy / Permission Boundary 등으로 설명

### Managed Identity ↔ IAM Role
- 애플리케이션 코드에 비밀번호/액세스키를 넣지 않는 방식
- Azure 리소스가 다른 Azure 서비스에 접근할 때 Managed Identity
- AWS에서는 보통 IAM Role 부여 방식으로 설명

Azure CLI는 서비스 주체(service principal)와 관리 ID(managed identity) 로그인도 지원합니다. `az login --service-principal ...` 및 `az login --identity` 같은 공식 예시가 제공됩니다. citeturn0search16turn0search0

---

## 9) 모니터링과 운영 비교

### Azure
- **Azure Monitor**: 전체 모니터링 플랫폼
- **Log Analytics**: 로그 조회/분석
- **Application Insights**: 애플리케이션 성능/APM

### AWS
- **CloudWatch**: 메트릭, 로그, 알람 중심
- **X-Ray**: 분산 추적/APM 성격 일부 보완

면접 답변 예시:

> "Azure에서는 Azure Monitor와 Application Insights로 앱 성능과 장애 분석을 했고, AWS 기준으로 설명하면 CloudWatch와 X-Ray 조합에 가깝다고 말할 수 있습니다."

---

## 10) Azure에도 AWS CLI 같은 도구가 있나?

있습니다.

### Azure CLI (`az`)
- Azure 공식 크로스플랫폼 CLI
- Windows, macOS, Linux 지원
- 브라우저 없이도 리소스 생성/조회/삭제/자동화 가능

### Azure PowerShell (`Az` 모듈)
- PowerShell 기반 자동화 도구
- PowerShell 친화적인 운영팀에서 선호

### Azure Cloud Shell
- Azure Portal에서 바로 실행 가능한 브라우저 기반 셸
- 로컬 설치 없이 Azure CLI / PowerShell 사용 가능

공식 문서에 따르면 Azure CLI는 cross-platform command-line tool이고, Azure CLI / Azure PowerShell / Azure Cloud Shell은 기능이 일부 겹치지만 동작 방식이 다르므로 용도에 따라 선택하라고 안내합니다. citeturn0search2turn0search12turn0search10

면접 답변 예시:

> "AWS CLI처럼 Azure에도 Azure CLI가 있습니다. 기본은 `az` 명령을 쓰고, PowerShell 중심 환경이면 Azure PowerShell도 많이 사용합니다. 포털 접근이 어려운 상황이나 자동화 시나리오에서는 CLI가 중요합니다."

---

## 11) AWS CLI vs Azure CLI 기본 흐름 비교

### 로그인 / 인증

#### AWS CLI
```bash
aws configure
aws sts get-caller-identity
```

#### Azure CLI
```bash
az login
az account show
```

AWS는 `aws configure` 또는 SSO 설정으로 자격증명을 구성하고 `aws sts get-caller-identity`로 현재 IAM 자격증명 정보를 확인할 수 있습니다. Azure는 `az login`으로 로그인하고 `az account show` 또는 Subscription 명령으로 현재 컨텍스트를 확인합니다. citeturn0search1turn0search15turn0search6

---

## 12) AWS CLI vs Azure CLI 명령어 비교표

> 아래 표는 **개념 대응표**입니다. 완전히 같은 기능이 아니라, 면접이나 실무에서 가장 자주 비교되는 흐름 기준으로 정리했습니다.

| 목적 | AWS CLI | Azure CLI | 설명 |
|---|---|---|---|
| 로그인 | `aws configure` / `aws sso login` | `az login` | 로컬 인증 구성 |
| 현재 계정/구독 확인 | `aws sts get-caller-identity` | `az account show` | 현재 인증 컨텍스트 확인 |
| 계정/구독 목록 조회 | 조직/프로필 기준 조회 | `az account list -o table` | Azure는 구독 목록 조회가 직관적 |
| 기본 계정/구독 전환 | `AWS_PROFILE=prod` 또는 profile 변경 | `az account set --subscription "<SUB_ID>"` | 작업 대상 전환 |
| VM 목록 조회 | `aws ec2 describe-instances` | `az vm list -d -o table` | 가상 서버 조회 |
| VM 생성 | `aws ec2 run-instances` | `az vm create ...` | IaaS 생성 |
| 오브젝트 스토리지 목록 | `aws s3 ls` | `az storage blob list ...` | S3 / Blob 비교 |
| 버킷/컨테이너 생성 | `aws s3 mb s3://bucket-name` | `az storage container create ...` | 스토리지 네임스페이스 생성 |
| 쿠버네티스 클러스터 자격증명 | `aws eks update-kubeconfig ...` | `az aks get-credentials ...` | kubectl 연결 |
| 함수 목록 조회 | `aws lambda list-functions` | `az functionapp list` | 서버리스 앱 조회 |
| RDB 인스턴스 조회 | `aws rds describe-db-instances` | `az sql server list` / `az sql db list` | 관리형 DB 조회 |
| 리소스 그룹/스택 배포 | `aws cloudformation deploy ...` | `az deployment group create ...` | IaC 배포 |
| 태그/리소스 그룹 관점 관리 | 태그/CloudFormation 중심 | `az group create` / `az group delete` | Azure는 RG 중심 |
| 로그 조회 | `aws logs describe-log-groups` 등 | `az monitor ...` | 모니터링/로그 조회 |

---

## 13) 자주 쓰는 CLI 예시 비교

### 13-1. 로그인과 컨텍스트 확인

#### AWS
```bash
aws configure
aws sts get-caller-identity
```

#### Azure
```bash
az login
az account show -o table
az account list -o table
az account set --subscription "<subscription-id>"
```

Azure 공식 문서에서는 `az login` 후 기본 Subscription이 표시되며, 다른 Subscription으로 바꾸려면 `az account set --subscription`을 사용하라고 안내합니다. citeturn0search6turn0search4

### 13-2. VM 조회/생성

#### AWS
```bash
aws ec2 describe-instances
```

#### Azure
```bash
az vm list -d -o table
az vm create \
  --resource-group rg-demo \
  --name vm-demo \
  --image Ubuntu2204 \
  --admin-username azureuser
```

### 13-3. 쿠버네티스 연결

#### AWS
```bash
aws eks update-kubeconfig --name my-eks-cluster --region ap-northeast-2
```

#### Azure
```bash
az aks get-credentials --resource-group rg-aks --name my-aks-cluster
```

### 13-4. 스토리지 조회

#### AWS
```bash
aws s3 ls
```

#### Azure
```bash
az storage account list -o table
az storage container list --account-name mystorageaccount -o table
```

### 13-5. 리소스 그룹 생성

#### AWS
AWS에는 Azure Resource Group과 완전히 같은 개념은 없습니다.
CloudFormation Stack, 태그, 프로젝트 단위 관리로 보완합니다.

#### Azure
```bash
az group create --name rg-demo --location koreacentral
az group list -o table
```

### 13-6. 서비스 주체 / 역할 기반 자동화

#### AWS
- IAM User Access Key 또는 IAM Role / SSO

#### Azure
```bash
az login --service-principal \
  --username <APP_ID> \
  --password <CLIENT_SECRET> \
  --tenant <TENANT_ID>
```

Azure CLI는 서비스 주체와 관리 ID 로그인 방식을 공식 지원하고, 대화형 사용자 로그인 대신 자동화에는 워크로드 ID나 관리 ID 사용을 권장합니다. citeturn0search16turn0search8turn0search0

---

## 14) Azure CLI vs Azure PowerShell 차이

### Azure CLI가 더 잘 맞는 경우
- 리눅스/맥/윈도우 공통 스크립트
- Bash 기반 자동화
- DevOps 파이프라인
- 빠른 실습

### Azure PowerShell이 더 잘 맞는 경우
- PowerShell 운영 환경
- Windows 관리 자동화
- 객체 지향 파이프라인 선호

Azure 공식 문서는 Azure CLI, Azure PowerShell, Azure Cloud Shell의 기능이 일부 겹치지만 언어/셸 환경이 달라 적합한 도구를 선택하라고 설명합니다. citeturn0search12

면접 답변 예시:

> "AWS에서 Bash 기반으로 AWS CLI를 쓰던 팀이라면 Azure에서도 Azure CLI가 가장 빠르게 적응됩니다. 반대로 Windows 운영팀 중심이면 Azure PowerShell 선호도가 높을 수 있습니다."

---

## 15) 면접에서 자주 나오는 비교 질문 30개와 답변 포인트

### 1. Azure Subscription은 AWS에서 무엇과 비슷한가?
- AWS Account와 가장 비슷
- 과금, 리소스 경계, 권한 관리의 핵심 단위

### 2. Resource Group은 왜 중요한가?
- 관련 리소스를 묶어 배포/삭제/권한관리/비용 관리하기 쉬움
- AWS에는 완전 동일한 개념이 없음

### 3. Azure VM과 EC2 차이는?
- 둘 다 IaaS
- 큰 차이보다 운영 방식과 주변 서비스 연동 차이를 말하면 좋음

### 4. App Service와 Elastic Beanstalk 차이는?
- 둘 다 앱 배포 플랫폼
- App Service가 더 PaaS스럽고 단순
- Beanstalk는 내부 인프라가 더 직접 보임

### 5. AKS와 EKS는 어떻게 비교하나?
- 둘 다 관리형 K8s
- 네트워크, IAM/ID 연동, 로깅 체계 차이를 설명하면 좋음

### 6. Azure Functions와 Lambda 차이는?
- 둘 다 서버리스
- 이벤트 기반, 짧은 실행, 자동 확장

### 7. VNet은 VPC와 같은가?
- 거의 같은 역할
- 주소 공간과 서브넷, 보안 설정의 기본 단위

### 8. NSG는 Security Group과 같은가?
- 가장 가까운 비교는 맞음
- 하지만 적용 범위와 모델은 완전히 같지 않음

### 9. Blob Storage는 S3와 같은가?
- 객체 스토리지 관점에서 가장 유사

### 10. Azure SQL은 AWS에서 무엇과 비슷한가?
- RDS와 가장 유사

### 11. Cosmos DB는 DynamoDB와 같은가?
- 가장 많이 비교되는 NoSQL 대응
- 완전 동일하다고 말하기보다 유사 범주라고 답변

### 12. Key Vault는 무엇과 비교할 수 있나?
- Secrets Manager + KMS를 함께 떠올리면 이해 쉬움

### 13. Managed Identity는 AWS에서 무엇과 같은가?
- IAM Role에 가장 가깝다

### 14. Azure RBAC와 IAM 차이는?
- 둘 다 권한관리 체계
- Azure는 Subscription / RG / Resource 계층 모델이 강조됨

### 15. Azure에도 CLI 자동화가 가능한가?
- 가능
- `az` 명령 기반 자동화, PowerShell, Cloud Shell까지 가능

### 16. Azure Cloud Shell은 무엇인가?
- 포털 안에서 바로 CLI/PowerShell 실행 가능한 브라우저 셸

### 17. AWS CLI처럼 구독 전환이 가능한가?
- 가능
- `az account list`, `az account set --subscription ...`

### 18. Azure에서도 IaC를 쓰나?
- 예
- Bicep, ARM, Terraform 많이 사용

### 19. ARM과 CloudFormation 비교는?
- Azure 전용 기본 IaC는 ARM/Bicep
- AWS는 CloudFormation

### 20. Terraform은 두 클라우드 모두에서 쓰나?
- 예
- 멀티클라우드 관점에서 강점

### 21. Azure 정적 웹 배포는 AWS와 어떻게 비교하나?
- Azure Static Web Apps 또는 Blob 정적 호스팅
- AWS는 S3 + CloudFront 조합이 대표적

### 22. Azure에서 로깅은 어떻게 보나?
- Azure Monitor, Log Analytics, App Insights 조합

### 23. AWS CloudWatch와 가장 가까운 Azure 서비스는?
- Azure Monitor 중심으로 설명

### 24. 글로벌 웹 진입점은 무엇을 쓰나?
- Azure Front Door
- AWS는 CloudFront 중심 비교

### 25. 관계형 DB와 NoSQL 선택 기준은?
- 정합성과 트랜잭션 중심이면 Azure SQL / RDS
- 대규모 저지연 확장이면 Cosmos DB / DynamoDB

### 26. 비밀값은 코드에 넣지 않는다면 어디에 두나?
- Azure Key Vault
- AWS에선 Secrets Manager/KMS

### 27. 자동화에서 사용자 계정보다 더 좋은 인증 방식은?
- Azure Managed Identity 또는 Service Principal
- AWS IAM Role / SSO / 워크로드 ID

### 28. Azure PowerShell 대신 Azure CLI를 쓰는 이유는?
- Bash 친화적이고 멀티플랫폼 자동화에 좋음

### 29. Azure App Service 대신 AKS를 선택하는 경우는?
- 컨테이너 표준화, 서비스 분리, 복잡한 오케스트레이션이 필요할 때

### 30. 면접에서 가장 중요한 비교 포인트는?
- 이름 암기가 아니라 선택 이유, 운영 복잡도, 비용, 보안, 확장성

---

## 16) 면접에서 바로 말하기 좋은 답변 문장

### 문장 1
> "AWS를 기준으로 보면 Azure Subscription은 Account에 가깝고, Resource Group은 Azure에서 리소스를 논리적으로 묶는 핵심 단위입니다."

### 문장 2
> "Azure App Service는 Elastic Beanstalk와 비슷하지만, 체감상 App Service가 더 관리형 PaaS에 가깝다고 설명할 수 있습니다."

### 문장 3
> "Azure Functions는 Lambda와 유사한 서버리스 서비스로, 이벤트 기반 처리나 예약 작업에 적합합니다."

### 문장 4
> "Azure Key Vault는 AWS의 Secrets Manager와 KMS를 함께 떠올리면 이해하기 쉽습니다."

### 문장 5
> "Azure에도 AWS CLI 같은 도구가 있고, 공식 CLI는 `az`입니다. 여기에 Azure PowerShell과 Azure Cloud Shell까지 운영 자동화 수단으로 같이 사용됩니다."

---

## 17) 최종 체크리스트

면접 전 마지막으로 아래를 점검하면 좋습니다.

- Azure 주요 서비스의 AWS 대응 관계를 설명할 수 있는가?
- 단순 매핑이 아니라 선택 이유까지 말할 수 있는가?
- `az login`, `az account set`, `az vm list`, `az aks get-credentials` 같은 기본 흐름을 아는가?
- Key Vault, Managed Identity, RBAC를 보안 관점에서 설명할 수 있는가?
- App Service / AKS / Functions를 상황에 따라 구분해 말할 수 있는가?
- Azure SQL / Cosmos DB를 비교해서 설명할 수 있는가?
- CloudWatch 경험을 Azure Monitor / App Insights로 연결해서 말할 수 있는가?

---

## 18) 한 줄 결론

**AWS를 알고 있다면 Azure 면접은 새 세상을 외우는 것이 아니라, 익숙한 개념을 Azure식 운영 모델로 번역해서 설명하는 준비**가 핵심입니다.

그리고 CLI 관점에서는,

- **AWS CLI ↔ Azure CLI(`az`)**
- **IAM Role ↔ Managed Identity**
- **CloudFormation ↔ ARM/Bicep**
- **S3 ↔ Blob Storage**
- **EC2 ↔ Azure VM**

이 축을 중심으로 정리하면 인터뷰 대응력이 훨씬 좋아집니다.
