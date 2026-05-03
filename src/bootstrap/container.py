from typing import Callable, Type, Any


class Container:
    """
    DI-контейнер с поддержкой factory и singleton binding.
    Реализует явное разделение стратегий создания зависимостей.
    """

    def __init__(self):
        self._resolving = set()
        self._factories: dict[Type, Callable[["Container"], Any]] = {}
        self._singletons: dict[Type, Any] = {}
        self._singleton_factories: dict[Type, Callable[["Container"], Any]] = {}

    def register(self, dependency: Type, provider: Callable[["Container"], Any]) -> None:
        """
        Регистрирует transient/factory зависимость.
        """
        self._factories[dependency] = provider

    def singleton(self, dependency: Type, provider: Callable[["Container"], Any]) -> None:
        """
        Регистрирует singleton зависимость.
        Инициализация происходит лениво при первом resolve.
        """
        self._singleton_factories[dependency] = provider

    def resolve(self, dependency: Type) -> Any:
        """
        Разрешает зависимость из контейнера.
        Поддерживает factory и singleton режимы.
        """
        if dependency in self._resolving:
            raise RuntimeError(f"Cyclic dependency detected: {dependency}")

        self._resolving.add(dependency)
        try:
            if dependency in self._singletons:
                return self._singletons[dependency]

            if dependency in self._singleton_factories:
                instance = self._singleton_factories[dependency](self)
                self._singletons[dependency] = instance
                return instance

            if dependency in self._factories:
                return self._factories[dependency](self)

            raise KeyError(f"No provider registered for {dependency}")
        finally:
            self._resolving.remove(dependency)