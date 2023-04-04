from writer_dynamodb_s3_website.write_dynamo import run_write_dynamodb
from reader_dynamodb_notification.read_dynamo import run_read_dynamo_sns
import threading
import sys

sec, diff_usd = int(sys.argv[1]), int(sys.argv[2])
print("Second ", sec)
print("Diff USD", diff_usd)

t_write = threading.Thread(target=run_write_dynamodb)
t_read = threading.Thread(target=run_read_dynamo_sns, args=(sec, diff_usd))

t_write.start()
t_read.start()
