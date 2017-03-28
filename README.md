esa_then_qiita
====

esa_then_qiita is the serverless application for cross posts to [esa.io](https://esa.io) and [Qiita](http://qiita.com). This application is mede with the [chalice](https://github.com/awslabs/chalice) by AWS.

* Create an esa.io post, send webhook to esa_then_qiita.
* If that post has a tag #qiita, and the same title post is not in you Qiita, automatically make a new Qiita post.
* Send result to Slack, when `SLACK_HOOK_URL` and `SLACK_CHANNEL` are set.


Usage
----

You can use this application for you esa.io and Qiita.

At first, `git clone` and make your config files.

```bash
$ git clone https://github.com/chroju/esa_then_qiita
$ cd esa_then_qiita
$ mv .chalice/config_sample.json .chalice/config.json
$ mv chalicelib/config_sample.json chalicelib/config.json
```

Edit `chalicelib/config.json`. If you don't need Slack integration, it is not necessary to set `SLACK_HOOK_URL` and `SLACK_CHANNEL`.

```json:config.json
{
  "QIITA_API_KEY": "aa123XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "SLACK_HOOK_URL": "https://hooks.slack.com/services/XXXXXX...",
  "SLACK_CHANNEL": "my_channel"
}
```

Install chalice, and deploy esa_then_qiita.

```python
$ pip install chalice
$ chalice deploy
Updating IAM policy.
Updating lambda function...
Regen deployment package...
Sending changes to lambda.
Lambda deploy done.
API Gateway rest API already found.
Deleting root resource id
Done deleting existing resources.
Deploying to: dev
https://XXXXXXXXXX.execute-api.ap-northeast-1.amazonaws.com/dev/
```

Set up esa.io generic webhook. URL is `https://XXXXXXXXXX.execute-api.ap-northeast-1.amazonaws.com/dev/qiita` (Don't forget method name `qiita`), and enable `on post create`. About esa.io generic webhook, refer to [dev/esa/webhooks/generic - docs.esa.io](https://docs.esa.io/posts/37).


License
----

MIT


Author
----

[chroju](https://chroju.net)
