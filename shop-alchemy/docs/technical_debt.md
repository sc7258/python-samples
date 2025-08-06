# 기술 부채 목록

이 문서는 당장 처리하지는 않지만, 추후 개선이 필요한 기술적인 이슈들을 기록한다.

- **Pydantic `Config` 클래스를 `ConfigDict`로 마이그레이션**
  - **이슈**: `pytest` 실행 시 `PydanticDeprecatedSince20` 경고 발생
  - **파일**: `src/application/schemas.py`
  - **내용**: Pydantic V2부터 `Config` 클래스 사용이 deprecated 되었다. V3에서 제거될 예정이므로, `ConfigDict`를 사용하도록 코드를 리팩토링해야 한다.
  - **우선순위**: 낮음 (현재 기능에 영향을 주지 않음)
