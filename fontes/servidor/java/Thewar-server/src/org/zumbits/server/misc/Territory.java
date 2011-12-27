/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package org.zumbits.server.misc;

/**
 *
 * @author joselito
 */
public class Territory {

    public static int TERRITORIES_ID[] =
        {1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
         11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
         21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
         31, 32, 33, 34, 35, 36, 37, 38, 39, 40,
         41, 42};

    private int _id;
    private int _name;
    private int _quantity;

    public Territory( int id, int quantity ) {
        _id = id;
        _quantity = quantity;
    }

    public int getId() {
        return _id;
    }

    public void setId(int _id) {
        this._id = _id;
    }

    public int getName() {
        return _name;
    }

    public void setName(int _name) {
        this._name = _name;
    }

    public int getQuantity() {
        return _quantity;
    }

    public void setQuantity(int _quantity) {
        this._quantity = _quantity;
    }

    

}
