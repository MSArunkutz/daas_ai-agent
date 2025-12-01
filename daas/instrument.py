from phoenix.otel import register
# import openinference_instrumentation.google_adk as _

tracer_provider = register(
    project_name="DAAS-App",
    endpoint="http://127.0.0.1:6006/v1/traces",
    auto_instrument=True
)

# tracer = tracer_provider.get_tracer(__name__)

# with tracer.start_as_current_span("smoke_test"):
#     pass