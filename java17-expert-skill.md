# Java 17 & Quarkus Expert Standards

## Dependency Injection (DI)
- **Constraint:** Use `private final` fields.
- **Pattern:** Use single-constructor injection. Do not use `@Inject` or `@Autowired` on the constructor if it's the only one (Quarkus standard).
- **Reject:** Any code using `@Autowired` on a field is considered a failure.

## Functional Programming
- **Lambda usage:** Always prefer `.stream().map().collect()` over `for` loops for data transformation.
- **Optional:** Use `Optional` for return types that can be null. Use `.ifPresentOrElse()` instead of `if (x != null)`.

## Quarkus Integrations
- **Kafka:** Map Spring `@KafkaListener` to `@Incoming`. Use `Record<K, V>` as the payload wrapper.
- **Camel:** Use the `LambdaRouteBuilder` (Camel 3.x/4.x style).
