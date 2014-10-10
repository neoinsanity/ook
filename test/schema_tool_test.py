from test_utils import base_test_case

from ontic import meta_type
from ontic.meta_type import PropertySchema
from ontic import schema_type
from ontic.schema_type import SchemaType
from ontic.validation_exception import ValidationException


class ValidateSchemaTestCase(base_test_case.BaseTestCase):
    """Test schema_types.validate_schema method."""

    def test_bad_validate_schema(self):
        """ValueError testing of validate_schema."""
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be provided.',
            schema_type.validate_schema, None)
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be of SchemaType.',
            schema_type.validate_schema, "not a schema")

    def test_validate_schema(self):
        """Valid schema testing of validate_schema."""
        schema = SchemaType({'some_property': {'type': 'int'}})

        # Dict test
        schema_type.validate_schema(schema)

        # OnticType test
        base_type_schema = SchemaType(schema)
        schema_type.validate_schema(base_type_schema)

        # SchemaType test
        schema_type_schema = SchemaType(schema)
        schema_type.validate_schema(schema_type_schema)

    def test_validate_schema_exception_handling(self):
        """Ensure validate_schema covers basic exception reporting."""
        property_schema = PropertySchema()
        property_schema.required = 'UNDEFINED'
        schema_instance = SchemaType()
        schema_instance.some_attr = property_schema

        self.assertRaisesRegexp(
            ValidationException,
            r"""The value for "required" is not """
            r"""of type "<type 'bool'>": UNDEFINED""",
            schema_type.validate_schema, schema_instance)

        expected_errors_list = [
            """The value for "required" is not of type "<type 'bool'>": UNDEFINED"""]

        try:
            schema_type.validate_schema(schema_instance)
            self.fail('A ValidationException should have been thrown.')
        except ValidationException as ve:
            self.assertListEqual(expected_errors_list, ve.validation_errors)

        errors = schema_type.validate_schema(
            schema_instance,
            raise_validation_exception=False)
        self.assertListEqual(expected_errors_list, errors)


class PerfectSchemaPropertyTestCase(base_test_case.BaseTestCase):
    """Test cases for the perfect_property_schema method."""

    def test_perfect_empty_schema_property(self):
        """Validate the perfection of an empty schema property."""
        candidate_schema_property = meta_type.PropertySchema()
        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
                'default': None,
                'enum': None,
                'member_max': None,
                'member_min': None,
                'member_type': None,
                'max': None,
                'min': None,
                'regex': None,
                'required': False,
                'type': None
            },
            candidate_schema_property)

        meta_type.perfect_property_schema(candidate_schema_property)

        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
                'regex': None,
                'member_max': None,
                'enum': None,
                'min': None,
                'default': None,
                'max': None,
                'required': False,
                'member_min': None,
                'member_type': None,
                'type': None
            }, candidate_schema_property)

    def test_perfect_partial_schema_property(self):
        """Validate the perfection of a partial schema definition."""
        candidate_schema_property = meta_type.PropertySchema(
            {
                'type': 'int',
                'required': True,
                'UNRECOGNIZED': 'irrelevant',
            })
        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
                'regex': None,
                'member_max': None,
                'enum': None,
                'min': None,
                'default': None,
                'max': None,
                'required': True,
                'member_min': None,
                'member_type': None,
                'type': int
            },
            candidate_schema_property)

        meta_type.perfect_property_schema(candidate_schema_property)

        self.assertEqual(10, len(candidate_schema_property))
        self.assertDictEqual(
            {
                'regex': None,
                'member_max': None,
                'enum': None,
                'min': None,
                'default': None,
                'max': None,
                'required': True,
                'member_min': None,
                'member_type': None,
                'type': int
            }, candidate_schema_property)

    def test_bad_perfect_schema_property(self):
        """Validate error handling for bad schemas passed to
        perfect_property_schema."""
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_property_schema" must be provided.',
            meta_type.perfect_property_schema, None)

        self.assertRaisesRegexp(
            ValueError,
            '"candidate_property_schema" must be PropertySchema type.',
            meta_type.perfect_property_schema, {})


class PerfectSchemaTestCase(base_test_case.BaseTestCase):
    """Test cases for use of the perfect_schema method."""

    def test_perfect_schema_type(self):
        """Validate 'perfect_schema' method usage."""
        candidate_schema = SchemaType({
            'prop1': meta_type.PropertySchema(),
            'prop2': meta_type.PropertySchema({'type': 'str', 'min': 5})
        })
        self.assertEqual(2, len(candidate_schema))
        self.assertEqual(10, len(candidate_schema.prop1))
        self.assertEqual(10, len(candidate_schema.prop2))
        self.maxDiff = None
        self.assertDictEqual(
            {
                'prop1': {
                    'regex': None,
                    'member_max': None,
                    'enum': None,
                    'min': None,
                    'default': None,
                    'max': None,
                    'required': False,
                    'member_min': None,
                    'member_type': None,
                    'type': None
                },
                'prop2': {
                    'regex': None,
                    'member_max': None,
                    'enum': None,
                    'min': 5.0,
                    'default': None,
                    'max': None,
                    'required': False,
                    'member_min': None,
                    'member_type': None,
                    'type': str
                }},
            candidate_schema)

        schema_type.perfect_schema(candidate_schema)

        self.assertEqual(2, len(candidate_schema))
        self.assertEqual(10, len(candidate_schema.prop1))
        self.assertEqual(10, len(candidate_schema.prop2))
        self.assertDictEqual(
            {
                'prop1': {
                    'default': None,
                    'enum': None,
                    'member_max': None,
                    'member_min': None,
                    'member_type': None,
                    'max': None,
                    'min': None,
                    'regex': None,
                    'required': False,
                    'type': None
                },
                'prop2': {
                    'default': None,
                    'enum': None,
                    'member_max': None,
                    'member_min': None,
                    'member_type': None,
                    'max': None,
                    'min': 5.0,
                    'regex': None,
                    'required': False,
                    'type': str
                }
            }, candidate_schema)
        self.assertIsInstance(candidate_schema.prop1, meta_type.PropertySchema)
        self.assertIsInstance(candidate_schema.prop2, meta_type.PropertySchema)

    def test_bad_perfect_schema(self):
        """Validate proper error handling in 'perfect_schema' method."""
        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be provided.',
            schema_type.perfect_schema, None)

        self.assertRaisesRegexp(
            ValueError,
            '"candidate_schema" must be of SchemaType.',
            schema_type.perfect_schema, {})