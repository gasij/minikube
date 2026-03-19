#!/usr/bin/env python3
from __future__ import annotations

import datetime as _dt
import html
import os
import zipfile


def _xml_escape(text: str) -> str:
    # WordprocessingML uses XML; also preserve leading/trailing spaces with xml:space.
    return html.escape(text, quote=False)


def _w_p(text: str, bold: bool = False) -> str:
    text_xml = _xml_escape(text)
    rpr = "<w:rPr><w:b/></w:rPr>" if bold else ""
    return (
        "<w:p>"
        "<w:pPr/>"
        "<w:r>"
        f"{rpr}"
        f'<w:t xml:space="preserve">{text_xml}</w:t>'
        "</w:r>"
        "</w:p>"
    )


def _w_codeblock(lines: list[str]) -> list[str]:
    # Simple monospace-like: keep as normal paragraphs with indentation marker.
    out: list[str] = []
    out.append(_w_p("Команды:", bold=True))
    for line in lines:
        out.append(_w_p(line))
    return out


def build_document_paragraphs() -> list[str]:
    today = _dt.date.today().strftime("%d.%m.%Y")

    paras: list[str] = []
    # Title page (GOST-like; simple layout)
    paras.append(_w_p("Федеральное государственное автономное образовательное учреждение", bold=False))
    paras.append(_w_p("высшего образования", bold=False))
    paras.append(_w_p("«НАЦИОНАЛЬНЫЙ ИССЛЕДОВАТЕЛЬСКИЙ ТОМСКИЙ ПОЛИТЕХНИЧЕСКИЙ УНИВЕРСИТЕТ»", bold=True))
    paras.append(_w_p(""))
    paras.append(_w_p("ОТЧЁТ", bold=True))
    paras.append(_w_p("по лабораторной работе", bold=True))
    paras.append(_w_p("Тема: Развертывание приложения в Kubernetes (Minikube). Blue/Green обновление", bold=False))
    paras.append(_w_p(""))
    paras.append(_w_p("Дисциплина: (укажите дисциплину)", bold=False))
    paras.append(_w_p(""))
    paras.append(_w_p("Выполнил: Жучков Иван Алексеевич, группа 10923-2", bold=False))
    paras.append(_w_p("Проверил: (укажите преподавателя)", bold=False))
    paras.append(_w_p(""))
    paras.append(_w_p(f"Томск — {today}", bold=False))
    # Page break after title
    paras.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    paras.append(_w_p("1. Цель работы", bold=True))
    paras.append(
        _w_p(
            "Подготовить манифесты Deployment и Service, развернуть приложение в Minikube, "
            "показать информацию о ресурсах и выполнить обновление версии по технологии blue/green."
        )
    )
    paras.append(_w_p(""))

    paras.append(_w_p("2. Оборудование и материалы", bold=True))
    for item in [
        "ПК с установленными Docker и Homebrew (macOS).",
        "Minikube и kubectl.",
        "Kubernetes-манифесты (Deployment/Service) и терминал.",
    ]:
        paras.append(_w_p(f"- {item}"))
    paras.append(_w_p(""))

    paras.append(_w_p("3. Ход работы", bold=True))
    paras.append(_w_p("3.1. Подготовка манифестов Kubernetes", bold=True))
    paras.append(_w_p("В проекте созданы файлы:"))
    for item in [
        "k8s/deployment-v1.yaml — Deployment версии v1 (10 реплик, requests/limits CPU+RAM).",
        "k8s/service-v1.yaml — Service версии v1 (NodePort 30080).",
        "k8s/deployment-v2.yaml — Deployment версии v2 (green) (10 реплик, requests/limits CPU+RAM).",
        "k8s/service-v2.yaml — Service версии v2 (NodePort 30081) для проверки green.",
        "k8s/myapp-service.yaml — общий Service (NodePort 30082) для переключения blue/green.",
        "scripts/minikube-deploy.sh — скрипт запуска/деплоя/переключения/дашборда.",
        "README.md — список всех команд и шагов.",
    ]:
        paras.append(_w_p(f"- {item}"))
    paras.append(_w_p(""))

    paras.append(_w_p("3.2. Соответствие манифестов требованиям задания", bold=True))
    for item in [
        "Название и селектор приложения: app=myapp, version=v1/v2 (labels + selector.matchLabels).",
        "Версия приложения: задаётся лейблом version и именем ресурсов (myapp-v1, myapp-v2).",
        "Количество реплик: replicas: 10.",
        "Выделение ресурсов: requests cpu=250m/memory=256Mi, limits cpu=500m/memory=512Mi.",
        "Service с версией: myapp-v1-service и myapp-v2-service.",
        "Проброс портов: Service port 80 -> targetPort контейнера (в текущем примере targetPort=80).",
    ]:
        paras.append(_w_p(f"- {item}"))
    paras.append(_w_p(""))

    paras.append(_w_p("3.3. Запуск кластера Minikube и развертывание", bold=True))
    paras.append(_w_p("Команды запуска кластера и деплоя приведены ниже."))
    paras.append(_w_p(""))

    paras.append(_w_p("4. Результаты и их анализ", bold=True))
    paras.append(
        _w_p(
            "Deployment поддерживает требуемое число Pod’ов и выполняет обновления через ReplicaSet. "
            "Service выбирает Pod’ы по selector и распределяет трафик на найденные endpoints."
        )
    )
    paras.append(_w_p("Blue/Green реализован так:"))
    for item in [
        "blue = версия v1 (Deployment myapp-v1).",
        "green = версия v2 (Deployment myapp-v2).",
        "общий Service myapp-service переключается изменением selector с version=v1 на version=v2.",
        "для проверки каждой версии отдельно используются myapp-v1-service и myapp-v2-service.",
    ]:
        paras.append(_w_p(f"- {item}"))
    paras.append(_w_p(""))

    paras.append(_w_p("5. Команды для выполнения работы", bold=True))
    paras.extend(
        _w_codeblock(
            [
                "cd /Users/soprano/codework/mikube",
                "",
                "# Установка Minikube (если нужно)",
                "brew install minikube",
                "",
                "# Запуск кластера",
                "minikube start --driver=docker",
                "",
                "# Деплой v1 + вывод информации",
                "chmod +x scripts/minikube-deploy.sh",
                "./scripts/minikube-deploy.sh deploy-v1",
                "kubectl get deployment myapp-v1",
                "kubectl get pods -l app=myapp,version=v1",
                "kubectl get service myapp-v1-service",
                "",
                "# Проверка доступа к v1",
                "minikube service myapp-v1-service --url",
                "",
                "# Деплой v2 (green) + вывод информации",
                "./scripts/minikube-deploy.sh deploy-v2",
                "kubectl get deployment myapp-v2",
                "kubectl get pods -l app=myapp,version=v2",
                "kubectl get service myapp-v2-service",
                "",
                "# Проверка green",
                "minikube service myapp-v2-service --url",
                "",
                "# Переключение blue -> green",
                "./scripts/minikube-deploy.sh switch",
                "",
                "# Проверка общего сервиса после переключения",
                "minikube service myapp-service --url",
                "",
                "# Дашборд",
                "minikube dashboard",
                "",
                "# (Опционально) очистка v1",
                "kubectl delete deployment myapp-v1",
                "kubectl delete service myapp-v1-service",
            ]
        )
    )
    paras.append(_w_p(""))

    paras.append(_w_p("6. Выводы", bold=True))
    paras.append(
        _w_p(
            "В ходе работы были подготовлены манифесты Deployment и Service, выполнен запуск кластера Minikube, "
            "развертывание двух версий приложения и переключение трафика по технологии blue/green. "
            "Поставленная цель работы достигнута."
        )
    )
    paras.append(_w_p(""))

    paras.append(_w_p("7. Примечания", bold=True))
    for item in [
        "NodePort должен быть уникальным: v1-service=30080, v2-service=30081, общий myapp-service=30082.",
        "Если pod’ы не запускаются, проверьте образ (ImagePullBackOff) и события: kubectl describe pod <имя>.",
        "Для реального приложения замените image и порты в deployment/service на ваши значения.",
    ]:
        paras.append(_w_p(f"- {item}"))

    return paras


def build_docx(output_path: str) -> None:
    # Minimal DOCX package with basic styles for GOST-like formatting:
    # - A4 margins: left 30mm, right 15mm, top/bottom 20mm
    # - Times New Roman 14pt
    # - line spacing 1.5
    # - justify, first line indent 1.25cm
    content_types = """<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
  <Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
  <Override PartName="/word/footer1.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.footer+xml"/>
</Types>
"""

    rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
"""

    document_rels = """<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdStyles" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
  <Relationship Id="rIdFooter1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/footer" Target="footer1.xml"/>
</Relationships>
"""

    styles = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:style w:type="paragraph" w:default="1" w:styleId="Normal">
    <w:name w:val="Normal"/>
    <w:qFormat/>
    <w:pPr>
      <w:jc w:val="both"/>
      <w:spacing w:line="360" w:lineRule="auto"/>
      <w:ind w:firstLine="709"/>
    </w:pPr>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:sz w:val="28"/>
      <w:szCs w:val="28"/>
      <w:color w:val="000000"/>
    </w:rPr>
  </w:style>
</w:styles>
"""

    footer1 = """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:ftr xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:p>
    <w:pPr><w:jc w:val="center"/></w:pPr>
    <w:r><w:fldChar w:fldCharType="begin"/></w:r>
    <w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>
    <w:r><w:fldChar w:fldCharType="end"/></w:r>
  </w:p>
</w:ftr>
"""

    paragraphs = "\n".join(build_document_paragraphs())
    document = f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
  <w:styles/>
  <w:body>
    {paragraphs}
    <w:sectPr>
      <w:pgSz w:w="11906" w:h="16838"/>
      <w:pgMar w:top="1134" w:right="850" w:bottom="1134" w:left="1701" w:header="708" w:footer="708" w:gutter="0"/>
      <w:titlePg/>
      <w:footerReference w:type="default" r:id="rIdFooter1" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"/>
    </w:sectPr>
  </w:body>
</w:document>
"""

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", content_types)
        z.writestr("_rels/.rels", rels)
        z.writestr("word/_rels/document.xml.rels", document_rels)
        z.writestr("word/styles.xml", styles)
        z.writestr("word/footer1.xml", footer1)
        z.writestr("word/document.xml", document)


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "..", "report.docx")
    out = os.path.abspath(out)
    build_docx(out)
    print(out)

