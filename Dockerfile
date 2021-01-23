#
# Build
#

FROM alpine:latest AS build

ADD https://languagetool.org/download/LanguageTool-stable.zip /
RUN apk add --no-cache zip && \
    unzip /LanguageTool-stable.zip -d /LT && \
    mv /LT/LanguageTool-* /LanguageTool

#
# RUN
#

FROM openjdk:14

WORKDIR /LanguageTool
COPY --from=build /LanguageTool .
EXPOSE 8080

CMD ["java", "-cp", "languagetool-server.jar", "org.languagetool.server.HTTPServer", "--port=8080", "--public", "--allow-origin=*"]
