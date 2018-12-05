from django.db import models


class App(models.Model):
    app = models.CharField(max_length=50)

    def __str__(self):
        return self.app


class Stream(models.Model):
    stream = models.CharField(max_length=100)

    def __str__(self):
        return self.stream


class Ts(models.Model):
    ts = models.BigIntegerField()
    duration = models.FloatField(max_length=5)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    stream = models.ForeignKey(Stream, on_delete=models.CASCADE)

    def __str__(self):
        return u'%s/%s/%s' % (self.app, self.stream, self.ts)

    class Meta:
        ordering = ['ts']
