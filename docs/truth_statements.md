# First Principles (Truth Statements)

The following is a list of truth statements about PyVeritas. All of these statements are true and therefore explain the behaviour of PyVeritas. These truth statemtents can be used to generate accurate documentation. 

## Meta

- If the `enabled` setting is set to `1` that specific test will run.
- If the `enabled` setting is set to `0` that specific test will not run.
- If the `enabled` setting is not part of the test's metadata (JSON) then the test will run by default. 

## Input

- [x] The input array can be empty or contain multiple items. 
- [x] Each item in the input array must have a `name`, and a `type`.
- [x] If a specific item in the `input` tuple has a `type` (only `int` and `float` are supported) and `range` (with valid `min` and `max` values) but no `value` then a suitable random `value` (within the specified range) will be created automatically by PyVeritas.
- If a specific item in the `input` tuple has a `type` (only `int` and `float` are supported) but no `value` then a suitable random `value` will be created automatically by PyVeritas.
- If all of the items in the `input` tuple have an explicit value, then the `iterations` is ignored. The `iterations` is only for fuzzing (where one or more input `value` is dynamically generated)
- If any of the items in the `input` tuple have a valid value in the `regular_expression` section and no explicit `value` then PyVeritas will generate a value for that item (in accordance with the regular expression specified). 
- If any of the items in the `input` tuple have a valid value in the `range` section and no explicit `value` then PyVeritas will generate a value for that item (in accordance with the `min` and `max`).
- If an explicit `value` is present, this `value` is used directly for unit testing and no value is generated for the particular that specific item in the `input`.
- The `type` specified must align with the `value`, `regular_expression` or the `range`'s `min` and `max` values, or PyVeritas will output an error message about how to better write the test's JSON.
- Value has the highest precedence, used for unit testing. In the absence of value, `regular_expression` takes next precedence.
- In the absence of `value` and `regular_expression`, `range`'s `min` and `max` take precedence.
- In the abcense of `value`, `regular_expression`, and `range` PyVeritas will automatically generate a random value based on the `type` specified.
- It is best for the JSON to only have either `value`, `regular_expression`, or `range` for simplicity and readability; and to avoid confusion. But if there are conflicting `value`, `regular_expression`, and `range` the precedence is always, `value` first, `regular_expression` second, and `range` third.
- All tests that contain at least one or more `regular_expression`, `range` or abcence of a `value` in the input tuple of the test will activate fuzzing on that particular test.
- If some items in the `input` tuple are explicit (have a `value`) and some items in the `input` do not, this will activate fuzzing.
- When fuzzing is activated a `value` is automatically generated but just as importantly the `iterations` value is in effect and the test will be repeated in accordance with the `iterations` number. If the `iterations` is missing when values are randomly generated then the default of `100` iterations will be in effect.
- During these repeat `iterations` any explicit `value` in the input tuple will obviously stay the same. Only the generated values will change for each iteration.
- The `iterations` setting is completely ignored if all of the `value`s in the in the `input` tuple are using an explicit and valid static `value`.

## Output

- If specified, `exception` and `exception_message` are checked against the actual exceptions thrown during testing.
- If not specified (or a blank string), then it is assumed that an `exception` and `exception_message` should not be thrown as part of the test (in this case a thrown exception will result in a failed test and an error message will help the user to write better JSON for their test).
- Both the `exception`'s type and the `exception_message` will be checked explicitly. If either or both of those are not an exact match for the `exception` instance and `exception_message` then the test fails.

## Iterations
Iterations only applies to fuzzing tests. 
Fuzzing occurs when any input uses regular_expression or range.
Tests with only explicit values always just run once.