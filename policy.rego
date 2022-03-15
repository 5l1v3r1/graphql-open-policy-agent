package graphql

default allow = false

privileged_fields := {"price", "discount_code"}

allow {
	input.user == "admin"
	field_allowed
}

field_allowed {
  privileged_fields[input.field]
}