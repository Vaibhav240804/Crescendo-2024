// imports

class UserController {
  constructor() { }

  testing = async (req, res) => {
    try {
        const { name } = req.body;
        const response = 'Hello ' + name;
        res.status(200).json({ message: "Hello World", response });
    } catch (error) {
        console.log(error);
        res.status(500).json({ message: "Internal Server Error" });
    }
  }
}

export default UserController;