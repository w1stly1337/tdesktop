import sys

target = sys.argv[1]
with open(target, 'r') as f:
    lines = f.readlines()

rsa_key = (
    '-----BEGIN RSA PUBLIC KEY-----\\n\\'
    'MIIBCgKCAQEA1J8JIDACtrn6ykiFHhJ4BQQCs32GkWjpfJOn8JVN7+gdthPi/ASU\\n\\'
    'FiXVwX9JBmKeZN9P2YvD9BVV/3y8QXa0no1l7iyUFfNbfbTyqaondZpZaH2/JxTA\\n\\'
    'RK1zZfPGKAbJaLMFUWR5vjjc4hBPXrVXb2AJ5u+RmHnDVI1aNJRKa+xe1DToaeAz\\n\\'
    '3aVT/0efIDqkdJ4oLUFYdjIT7HmICIuYwBX3GTOCTnmzMCWpQe8iHvhUnUR2z2of\\n\\'
    'jeaRIFUREV3JSFu39BPVoyGif05heaW4wVRe6r7XJa7DzN26taCp+6OsNbps8LaI\\n\\'
    '1skv9OyrwrAOaEb6CTMEE7BdrXSW2PPtzQIDAQAB\\n\\'
    '-----END RSA PUBLIC KEY-----'
)

test_line = 'const char *kTestPublicRSAKeys[] = { "' + rsa_key + '" };'
pub_line = 'const char *kPublicRSAKeys[] = { "' + rsa_key + '" };'

result = []
skip = False
inserted = False
i = 0
while i < len(lines):
    line = lines[i]
    if not skip and 'kTestPublicRSAKeys' in line and '[]' in line:
        skip = True
        result.append(test_line + '\n')
        result.append(pub_line + '\n')
        inserted = True
        i += 1
        continue
    if not skip and 'kPublicRSAKeys' in line and '[]' in line:
        skip = True
        i += 1
        continue
    if skip and '-----END RSA PUBLIC KEY-----' in line and '};' in line:
        skip = False
        i += 1
        continue
    if skip:
        i += 1
        continue
    result.append(line)
    i += 1

assert inserted, 'Never found kTestPublicRSAKeys to replace'

with open(target, 'w') as f:
    f.writelines(result)

with open(target, 'r') as f:
    content = f.read()
assert content.count('MIIBCgKCAQEA1J8JIDACtrn6') == 2, 'RSA key count wrong: ' + str(content.count('MIIBCgKCAQEA1J8JIDACtrn6'))
assert '} // namespace' in content, 'namespace brace missing'
print('RSA patch OK')
