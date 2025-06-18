import unittest
import os
import tempfile
import yaml
import json
from pathlib import Path
from generate_yaml_schema_doc import load_yaml, build_desc_map, generate_markdown

class TestGenerateYamlSchemaDoc(unittest.TestCase):

    def setUp(self):
        # テスト用のYAMLデータとスキーマを準備
        self.sample_yaml = {
            'session': {
                'phase1': 'trust building',
                'phase2': 'reframing'
            }
        }
        self.sample_schema = {
            "type": "object",
            "properties": {
                "session": {
                    "type": "object",
                    "description": "A full session structure",
                    "properties": {
                        "phase1": {
                            "type": "string",
                            "description": "First phase of the session"
                        },
                        "phase2": {
                            "type": "string",
                            "description": "Second phase of the session"
                        }
                    }
                }
            }
        }

        # 一時ファイルを作成して保存
        self.yaml_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.yaml')
        yaml.dump(self.sample_yaml, self.yaml_file)
        self.yaml_file.close()

        self.schema_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.json')
        json.dump(self.sample_schema, self.schema_file)
        self.schema_file.close()

        self.output_file = tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.md')
        self.output_file.close()

    def tearDown(self):
        os.unlink(self.yaml_file.name)
        os.unlink(self.schema_file.name)
        os.unlink(self.output_file.name)

    def test_load_yaml(self):
        data = load_yaml(Path(self.yaml_file.name))
        self.assertIn('session', data)
        self.assertIn('phase1', data['session'])

    def test_build_desc_map(self):
        schema = load_yaml(Path(self.schema_file.name))
        desc_map = build_desc_map(schema)
        self.assertIn('session.phase1', desc_map)
        self.assertEqual(desc_map['session.phase1'], 'First phase of the session')

    def test_generate_markdown(self):
        yaml_data = load_yaml(Path(self.yaml_file.name))
        schema_data = load_yaml(Path(self.schema_file.name))
        desc_map = build_desc_map(schema_data)
        md = generate_markdown(yaml_data, desc_map)
        self.assertIn('# session', md)
        self.assertIn('session.phase1', md)
        self.assertIn('First phase of the session', md)

if __name__ == '__main__':
    unittest.main()
