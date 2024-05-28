

## eBPF powered Network Service and Security Observability for Kubernetes

### Autorzy:

- Jakub Cudak
- Piotr Aksamit
- Karol Jurzec
- Paweł Zaręba

### Rok: 2024
### Grupa: gr.5

## Spis treści

1. [Wprowadzenie](#wprowadzenie)
2. [Podstawy teoretyczne / Stos technologiczny](#podstawy-teoretyczne--stos-technologiczny)
3. [Opis koncepcji Case Study](#opis-koncepcji-case-study)




4. [Architektura rozwiązania](#architektura-rozwiązania)
5. [Opis konfiguracji środowiska](#opis-konfiguracji-środowiska)
6. [Metody instalacji](#metody-instalacji)
7. [Jak odtworzyć? - krok po kroku](#jak-odtworzyć---krok-po-kroku)
    - 7.1. Podejście infrastruktury jako kod
8. [Kroki wdrożenia demo](#kroki-wdrożenia-demo)
    - 8.1. Konfiguracja ustawień
    - 8.2. Przygotowanie danych
    - 8.3. Procedura wykonania
    - 8.4. Prezentacja wyników
9. [Podsumowanie - wnioski](#podsumowanie---wnioski)
10. [Źródła](#źródła)

## Wprowadzenie

Hubble to zaawansowane narzędzie do obserwacji i nadzoru bezpieczeństwa w sieci. Jest zaprojektowane specjalnie dla
środowiska Kubernetes i opiera swoje działanie na technologii eBPF (Extended Berkeley Packet Filter). To rozwiązanie
umożliwia pełną widoczność i śledzenie ruchu sieciowego w czasie rzeczywistym, oferując niezbędne informacje do
monitorowania wydajności, debugowania problemów oraz zapewniania bezpieczeństwa zwłaszcza w rozbudowanej sieci aplikacji
mikroserwisowych. Celem tej pracy jest zapoznanie się z technologią Hubble oraz zaprezentowanie jej możliwości na
przykładzie konkretnego zbioru serwisów działających w środowisku Kubernetes.

## Podstawy teoretyczne / Stos technologiczny

Hubbel zbudowany jest na bazie technologi Cilium i eBPF, które umożliwiają głęboki wgląd w komunikację i zachowanie usług, a także infrastrukturę sieciową w całkowicie przejrzysty sposób.

Cilium jest oprogramowaniem open source służącym do zabezpieczania łączności sieciowej pomiędzy usługami aplikacji wdrożonymi przy użyciu platform zarządzania konteneramit takimi jak Docker i Kubernetes. Jego podstawą jest technologia jądra Linuksa zwana eBPF, która umożliwia dynamiczne wprowadzanie logiki kontroli bezpieczeństwa i kontroli w samym Linuksie. 

Głównym celem eBPF jset bezpieczne i wydajne rozszerzenie możliwości jądra w czasie wykonywania, bez konieczności wprowadzania zmian w kodzie źródłowym jądra lub ładowania jego modułów. Bezpieczeństwo zapewnia wbudowany w jądro weryfikator, który przeprowadza statyczną analizę kodu i odrzuca programy, które ulegają awarii, zawieszają się lub w inny sposób negatywnie wpływają na jądro.

Hubbel ponadto posiada swój graficzny interfejs instalowany jako część głównego serwisu. Pozwala on na automatyczne wykrywanie wykresu zależności usług dla klastrów Kubernetes, umożliwiając przyjazną dla użytkownika wizualizację i filtrowanie przepływów danych jako mapy usług.


Zdecydowaliśmy się na uzycie następującego stosu technologicznego:
- Minikube
- MongoDB
- Python + FastAPI
- NodeJS
- Hubble

## Opis koncepcji Case Study

Usługi:
- 1 sewer mongo db
- 3 serwery w pythonie 
- Hubble 

Koncept:
Monitorowanie, obciążenie procesora, ramu poprzez ciąg odpytywanie bazy danych i innych serwerów. 

Serwery:
- serwer 3 odpytuje serwer 2 i nie oczekuje na odpowiedź
- serwer 2 odpytuje serwer 1 i czeka na odpowiedź
- serwer 1 odpytuje mongo db i też czeka na odpowiedź

## Architektura rozwiązania

Zdecydowaliśmy się na analizę ruchu sieciowego w środowisku symulującym mikroserwisową aplikację uzywającą bazy danych MongoDB.
Architektura będzie wyglądała następująco:
![architecture](img/arch_overview.png)

Zrealizujemy 3 serwisy symulujące środowisko produkcyjne, które będą porozumiewać się ze sobą za pomocą protokołu http.
Serwisy zostaną zrealizowane w technologiach Python i/lub JavaScript.
Będą one generowały obciąenie rzędu kilku-kilkunastu zapytań na sekundę,
co pozwoli na satysfakcjonujące wyniki obserwacji.

W późniejszym stadium pracy mozemy wykonać migrację na klastrowy deployment mongodb (prawdopodobnie PSA),
w celu obserwacji komunikacji pomiędzy węzłami klastra bazodanowego.

## Opis konfiguracji środowiska
1 dockerfile, wszystkie usługi uruchomiane w jednym kontenerze. Takie podejście powoduje prostą konfiguracje i zarządzanie

## Kubectl
Kubectl to narzędzie do interakcji z klastrem k8s. Będziemy go często potrzebować.
Aby go zainstalować (zakładając środowisko Linux, x86), wykonaj:
```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
```

## Minikube
Minikube to lokalny klaster k8s, którego będziemy używać w tym projekcie.
Instrukcja instalacji znajduje się tutaj: https://minikube.sigs.k8s.io/docs/start/
Jeśli jesteś leniwy, możesz skopiować i wkleić te polecenia (zakładając środowisko Linux, x86):
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube && rm minikube-linux-amd64
```

Po tym możesz uruchomić klaster za pomocą `minikube start` - będzie potrzebował jakiegoś sterownika, Docker będzie w porządku, ponieważ jest preferowaną opcją (alternatywnie, możesz użyć podman). Minikube obsługuje wiele backendów (zobacz tutaj: https://minikube.sigs.k8s.io/docs/drivers/), ale nie będziemy się tym przejmować.

## Helm
Helm można traktować jako "menedżera pakietów dla Kubernetes". Wiele aplikacji dostarcza tzw. "chart Helm", czyli gotowy przepis na wdrożenie aplikacji do klastra k8s. Te charty Helm mają zestaw domyślnych wartości, które można nadpisać (jak ma to miejsce w tym projekcie).
Będziesz musiał zainstalować Helm na swoim lokalnym systemie, więc oto jak to zrobić (instrukcja: https://helm.sh/docs/intro/install/):
```bash
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3
chmod 700 get_helm.sh
./get_helm.sh
```

## MongoDB
Teraz, gdy nasze środowisko jest gotowe do pracy, możemy zacząć instalować usługi k8s.
Na początek będziemy musieli dodać kilka repozytoriów Helm do naszego systemu. Ten projekt będzie używał dwóch: repozytorium `bitnami`, które dostarcza większość powszechnie używanych usług, oraz repozytorium `cowboysysop`, które dostarcza Mongo Express - webowe GUI, które umożliwia interakcję z instalacją MongoDB.

Aby dodać repozytoria:

To add the repositories:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add cowboysysop https://cowboysysop.github.io/charts/
helm repo update # pull the data from newly added repositories
```

Po skonfigurowaniu wszystkiego możemy przystąpić do instalacji MongoDB w naszym lokalnym klastrze k8s. Na potrzeby tego projektu użyjemy architektury PSA (więcej informacji można znaleźć tutaj: https://www.mongodb.com/docs/v4.0/core/replica-set-architecture-three-members/#primary-with-a-secondary-and-an-arbiter-psa).

Aby zainstalować tę usługę za pomocą Helm, wykonaj następujące polecenie:

```bash
helm install mongo bitnami/mongodb -f mongo_values.yaml
```

Po tym możesz sprawdzić, czy k8s pods zostały poprawnie utworzone za pomocą `kubectl get pods -w` (-w oznacza watch).
Pamiętaj, że ta instalacja utworzy 8GB PVC (persistent volume claim) na Twoim lokalnym systemie plików.

Aby faktycznie interagować z naszą instalacją, skorzystamy z Mongo Express. Zainstaluj go za pomocą:
```bash
helm install mongo-express cowboysysop/mongo-express -f mongo_express_values.yaml
```

Ponownie, możemy sprawdzić, czy pod został poprawnie zainicjalizowany za pomocą `kubectl get pods -w`.

Aby uzyskać dostęp do webowego GUI z przeglądarki, musisz wykonać następujące polecenie:

bash


```bash
kubectl port-forward <the name of the mongo-express pod> 8081:8081
```
Teraz możesz uzyskać dostęp do GUI, odwiedzając `localhost:8081` w swojej przeglądarce.

## Podsumowanie - wnioski

## Źródła
