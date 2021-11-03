<h1 align="center">Welcome to simple benchmarking 👋</h1>
<p>
  <a href="https://www.npmjs.com/package/benchmarking" target="_blank">
    <img alt="Version" src="https://img.shields.io/npm/v/benchmarking.svg">
  </a>
  <a href="LICENSE" target="_blank">
    <img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-yellow.svg" />
  </a>
  <a href="https://twitter.com/zmastylo" target="_blank">
    <img alt="Twitter: zmastylo" src="https://img.shields.io/twitter/follow/zmastylo.svg?style=social" />
  </a>
</p>

> Thread pool allowing for status check i.e. are all threads busy?


## Basic Usage

```
    tp = ThreadPool(max_workers=5)
    
    # submit work
    func = time.sleep
    for _ in range(10):
        tp.submit(func, 3)

    # check if tp is busy
    if tp.busy():
        print("tp is busy")
    else:
        print("tp is not busy")
```

## Run tests
From threadpool directory:

```sh
export PYTHONPATH=. && pytest tests
```

## Author

👤 **Zbigniew Mastylo**

* Twitter: [@zmastylo](https://twitter.com/zmastylo)
* Github: [@zmastylo](https://github.com/zmastylo)
* LinkedIn: [@zmastylo](https://linkedin.com/in/zmastylo)

## Show your support

Give a ⭐️ if this project helped you!

## 📝 License

Copyright © 2021 [Zbigniew Mastylo](https://github.com/zmastylo).<br />
This project is [MIT](LICENSE) licensed.

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_
