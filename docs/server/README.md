# Server documentation

## Packet

A packet is a dict. Each of properties by following:

### "name"

- `grading-begin`: [self.on_grading_begin](./packet%20type/grading-begin.md),
- `grading-end`: [self.on_grading_end](./packet%20type/simple.md),
- `compile-error`: [self.on_compile_error](./packet%20type/compile-error.md),
- `compile-message`: [self.on_compile_message](./packet%20type/compile-message.md),
- `batch-begin`: [self.on_batch_begin](./packet%20type/simple.md),
- `batch-end`: [self.on_batch_end](./packet%20type/simple.md),
- `test-case-status`: [self.on_test_case](./packet%20type/test-case-status.md),
- `internal-error`: [self.on_internal_error](./packet%20type/internal-error.md),
- `submission-terminated`: [self.on_submission_terminated](./packet%20type/simple.md),
- `submission-acknowledged`: [self.on_submission_acknowledged](./packet%20type/simple.md),
- `ping-response`: [self.on_ping_response](./packet%20type/ping-response.md),
- `supported-problems`: [self.on_supported_problems](./packet%20type/supported-problems.md),
- `handshake`: [self.on_handshake](./packet%20type/handshake.md)
