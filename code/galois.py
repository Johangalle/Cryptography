#!/usr/bin/python3
#
# Galois addition and multiplication of polynomials.
# The coefficients of the polynomial are in modulo m.
# Most of the time, the coefficients are in modulo 2.
# Thjis module has not been tested extensively for moduli different from 2.
#
# The theory behind this can be found in many books describing finite field arithmetic.
# I always recommend WIlliam Stallings' Cryptography and Network Security, but for this particular topic, there is
# probably more specific course material.
#
# If anyone would need subtraction, this can be achieved by using the unary - operator (which is defined) combined with addition.
# If anyone would need division, this can be achieved by using the inverse function combined with multiplication.
#
# Written by Johan Galle
#
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/
#
# No part of this module should be used for cryptography in production.
# This module is strictly for education purposes.
#
import copy
class Polynomial:
    def __init__(self, modulo, *coefficients):
        """ input: coefficients are in the form a_n, ...a_1, a_0
            Do not forget to add trailing zero's
            Leading zero's are not meaningfull and are ignored (but not deleted).
        """
        self.coefficients = list()
        for coeff in coefficients:
            self.coefficients.append(coeff%modulo)
        self.modulo = modulo
        self.irreducible_polynomial = None

    def __repr__(self):
        """
        method to return the canonical string representation of a polynomial.
        Examples:
        1*x^3+2*x^2+3*x+0
        0
        The last coefficient is always printed
        """
        n = self.degree()
        string_rep = "Polynomial (modulo " + str(self.modulo) + ") : "
        string_orig_rep = string_rep
        for coeff in self.coefficients:
            if n == 0:
                string_rep = string_rep + str(coeff)
            elif coeff == 0:
                pass
            elif n == 1:
                string_rep = string_rep + str(coeff) + "*x" + "+"
            else:
                string_rep = string_rep + str(coeff) + "*x^" + str(n) + "+"
            n = n - 1
        if string_rep == string_orig_rep:
            string_rep = string_rep + "0"
        return string_rep
        
    def set_irreducible_polynomial(self, poly):
        self.irreducible_polynomial = poly
        
    def degree(self):
        """
        method to return the maximum degree of this polynomial
        The first coefficient may be zero, so this is not really the degree
        """
        return len(self.coefficients)-1
        
    def real_degree(self):
        """
        method to return the correct degree of this polynomial
        This method returns the correct result even if the first coefficient would be zero
        If all coefficients are zero, this method returns -1
        """
        deg = len(self.coefficients)-1
        while self.get_coeff_value(deg) == 0 and deg > 0:
            deg = deg - 1
        if self.get_coeff_value(deg) != 0:
            return deg
        else:
            return deg - 1

    def __add__(self, obj):
        """
        method to return a new Polynomial object with the resulting addition
        """
        degree = max(self.degree(),obj.degree())
        if self.modulo != obj.modulo:
            raise ValueError ("addition of polynomials requires identical moduli")
        if self.degree() == degree:
            result = copy.deepcopy(self)
            b = obj
        else:
            result = copy.deepcopy(obj)
            b = self
        offset = b.degree() + 1
        for coeff in b.coefficients:
            result.coefficients[-offset] = (result.coefficients[-offset] + coeff)%self.modulo
            offset = offset - 1
        return result
        
    def __neg__(self):
        """
        method to return a new Polynomial object that is the negative unary operator
        """
        result = Polynomial(self.modulo,0)
        l = list()
        for coeff in self.coefficients:
            l.append(-coeff%self.modulo)
        result.coefficients = l
        return result
    
    def get_coeff_value(self,i):
        """
        method to return the value of the coefficient related to the given degree
        If the polynomial is of a smller degree, return the value 0
        """
        if i > self.degree():
            return 0
        else:
            offset = i + 1
            return self.coefficients[-offset]
    
    def __eq__(self,obj):
        """
        method to compare values of two polynomials
        """
        if obj == None:
            return False
        result = (self.modulo == obj.modulo)
        offset = 0
        max_degree = max(self.degree(),obj.degree())
        while result and offset <= max_degree:
            result = result and (self.get_coeff_value(offset) == obj.get_coeff_value(offset))
            offset = offset + 1
        return result
        
    def __ne__(self,obj):
        """
        method to compare values of two polynomials
        """
        return not self == obj
        
    def factor(self,n):
        """
        method to return a new polynomial that is the result of the multiplication of the scamar n with the given polynomial
        """
        result = copy.deepcopy(self)
        index = 0
        for coeff in self.coefficients:
            result.coefficients[index] = coeff * n % self.modulo
            index = index + 1
        return result
        
    def timesx(self):
        if self.irreducible_polynomial == None:
            raise ValueError ("multiplication of polynomials requiresirreducible polynomial")
        if self.modulo != self.irreducible_polynomial.modulo:
            raise ValueError ("multiplication of polynomials requires moduli of irreducible polynomial and polynomial to be equal")
        if self.real_degree() >= self.irreducible_polynomial.real_degree():
            raise ValueError ("multiplication of polynomials requires an irreducible polynomial of higher degree")
        result = copy.deepcopy(self)
        result.coefficients.append(0)
        nr = 0
        while result.real_degree() == self.irreducible_polynomial.real_degree() and nr < self.modulo:
            result = result + self.irreducible_polynomial
            nr = nr + 1
        if nr == self.modulo:
            raise ValueError("Impossible timesx multiplication: is the irreducible polynomial really irreducible?")
        return result
        
    def __mul__(self,obj):
        """
        method to return a new Polynomial object with the resulting multiplication
        Such multiplication requires an irreducible polynomial
        """
        degree = max(self.real_degree(),obj.real_degree())
        if self.modulo != obj.modulo:
            raise ValueError ("multiplication of polynomials requires identical moduli")
        if self.irreducible_polynomial != obj.irreducible_polynomial:
            raise ValueError ("multiplication of polynomials requires identical irreducible polynomials")
        if self.irreducible_polynomial == None:
            raise ValueError ("multiplication of polynomials requires setting irreducible polynomials")
        if degree >= self.irreducible_polynomial.real_degree():
            raise ValueError("Multiplication of polynomials requires irredicuble polynomial of at least one degree higher than the highest degree of the polynomial terms of the multiplication")
        if self.real_degree() == degree:
            highest_degree_poly = self
            lowest_degree_poly = obj
        else:
            highest_degree_poly = obj
            lowest_degree_poly = self
        lowest_degree = lowest_degree_poly.real_degree()
        multiplication_table = list()
        multiplication_table.append(highest_degree_poly)
        for i in range(1, lowest_degree+1):
            multiplication_table.append(multiplication_table[i-1].timesx())
        result = Polynomial(self.modulo,0)
        start = 0
        for i in range(lowest_degree,-1,-1):
            result = result + multiplication_table[i].factor(lowest_degree_poly.get_coeff_value(i))
        result.irreducible_polynomial = self.irreducible_polynomial
        return result
        
    def to_int(self):
        """
        Method to calculate integer value corresponding to a polynomial
        The conversion is that the binary value corresponds with the coefficients of the polynomial.
        So, e.g. 37 = 100101 = x^5+x^2+1
        """
        base = 2
        value = 1
        result = 0
        for i in range(0,self.real_degree()+1):
            result = result + self.get_coeff_value(i)*value
            value = value*base
        return result
        
    def mult_inv(self):
        """
        When we work in GF(n), we know that a^(n-1) is always 1, so a^-1 = a^(n-2)
        When working in GF(2^k), n = 2^k, so a^-1 = a^(2^k-2)
        """
        degree = self.irreducible_polynomial.real_degree()
        exponent = self.modulo**degree - 2
        result = Polynomial(self.modulo,1)
        result.set_irreducible_polynomial(self.irreducible_polynomial)
        # For simplicity, I calculate the power to exponent by multiplying exponent times
        for index in range(0,exponent):
            result = result*self
        return result
        
def poly_from_int(nr):
    """
    Function to convert integer value to polynomial in modulo 2
    The conversion is that the binary value corresponds with the coefficients of the polynomial.
    So, e.g. 37 = 100101 = x^5+x^2+1
    """
    l = [int(i) for i in bin(nr)[2:]]
    result = Polynomial(2,0)
    result.coefficients = l
    return result
    
def galois_multiply(i,j,irred):
    ip = poly_from_int(i)
    ip.set_irreducible_polynomial(irred)
    jp = poly_from_int(j)
    jp.set_irreducible_polynomial(irred)
    resp = ip*jp
    return resp.to_int()
    
def galois_inverse(i,irred):
    ip = poly_from_int(i)
    ip.set_irreducible_polynomial(irred)
    jp = ip.mult_inv()
    j = jp.to_int()
    return j
                
if __name__ == "__main__":
    p = Polynomial(5,1,2,3,4)
    q = Polynomial(5,1,2,3,4)
    assert(p==q)
    res1 = p+q
    res2 = q+p
    assert(res1 == res2)
    assert(res1 != p)
    assert(res2 != p)
    
    p = Polynomial(2,1,2,3,4)
    q = Polynomial(2,1,2,3,4)
    zero = Polynomial(2,0)
    assert(p==q)
    res1 = p+q
    res2 = q+p
    assert(res1 == res2)
    assert(res1 != p)
    assert(res2 != p)
    assert(res1 == zero)

    p = Polynomial(5,1,2,3,4)
    q = -p
    assert(p!=q)
    res1 = p+q
    res2 = q+p
    assert(res1 == res2)
    zero = Polynomial(5,0)
    assert(res1 != p)
    assert(res2 != p)
    assert(res1 == zero)

    p = Polynomial(2,1,2,3,4)   #x^3 + x
    q = -p                      #x^3 + x
    assert(p==q)
    res1 = p+q
    res2 = q+p
    assert(res1 == res2)
    zero = Polynomial(2,0)
    assert(res1 != p)
    assert(res2 != p)
    assert(res1 == zero)
    assert(res1.real_degree()==-1)

    irred4 = Polynomial(2,1,0,0,1,1)   #x^4 + x + 1
    p.set_irreducible_polynomial(irred4)
    q1 = p.timesx()               #x*(x^3+x) = x^4 + x^2 + x^4 + x + 1 = x^2 + x + 1
    expected = Polynomial(2,1,1,1)
    assert(q1==expected)
    q2 = Polynomial(2,1,0)              #x
    q2.set_irreducible_polynomial(irred4)
    res = q2*p
    assert(res==expected)

    p = Polynomial(2,1,0,0,1,0,1,0,1)   #x^7+x^4+x^2+1
    q = Polynomial(2,1,0,0,0,1,0,1,0)   #z^7+x^3+x
    irred8 = Polynomial(2,1,0,0,0,1,1,0,1,1)    #x^8+x^4+x^3+x+1
    p.set_irreducible_polynomial(irred8)
    q.set_irreducible_polynomial(irred8)
    res = p * q
    expected = Polynomial(2,1)         #1
    assert(res==expected)

    p = Polynomial(2,1,0,1)   #x^2+1
    q = Polynomial(2,1,1,0)   #x^2+x
    irred3 = Polynomial(2,1,0,1,1)    #x^3+x+1
    p.set_irreducible_polynomial(irred3)
    q.set_irreducible_polynomial(irred3)
    res = p * q
    expected = Polynomial(2,1,1)         #x+1
    assert(res==expected)
    val = res.to_int()
    assert (val == 3)
    val = p.to_int()
    assert(val==5)
    val = q.to_int()
    assert (val == 6)
    
    poly = poly_from_int(3)
    assert(poly == res)
    poly = poly_from_int(5)
    assert(poly == p)
    poly = poly_from_int(6)
    assert(poly == q)

    res = galois_multiply(0x95,0x8a,irred8)
    assert(res == 1)
    res = galois_multiply(5,6,irred3)
    assert(res == 3)
    res = galois_multiply(3,6,irred3)
    assert (res == 1)
    res = galois_multiply(3,3,irred3)
    assert(res == 5)
    
    irred5 = Polynomial(2,1,1,1,0,1,1)
    res = galois_multiply(10,20,irred5)
    assert(res==18)
    res = galois_multiply(10,4,irred5)
    assert(res==19)
    res = galois_multiply(10,31,irred5)
    assert(res==17)
    res = galois_multiply(31,31,irred5)
    assert(res==23)
    
    res = galois_multiply(255,255,irred8)
    assert(res==19)
    res = galois_multiply(250,255,irred8)
    assert(res==61)
    res = galois_multiply(245,255,irred8)
    assert(res==79)
    res = galois_multiply(245,245,irred8)
    assert(res==87)
    res = galois_multiply(237,245,irred8)
    assert(res==119)
    res = galois_multiply(228,252,irred8)
    assert(res==238)
    res = galois_multiply(0,252,irred8)
    assert(res==0)
    res = galois_multiply(0,0,irred8)
    assert(res==0)
    res = galois_multiply(228,1,irred8)
    assert(res==228)

    # According to Fermat, any B^255 must be equal to 1 in GF(2^8).
    p = poly_from_int(219)
    one = Polynomial(2,1)
    res = Polynomial(2,1)
    res.set_irreducible_polynomial(irred8)
    p.set_irreducible_polynomial(irred8)
    # Of course, this is a very ineffcient way of calculating B^255 as it requires 255 multiplications
    # it would be far better to calculate B^128*B^64*B^32*B^16*B^8*B^4*B^2*B^1 and to calculate B^2^2^2^2^2^2^2^2,
    # which requires only 15 multiplications, but the goal here is to test the module
    for i in range(0,255):
        res = res*p
    assert (res==one)
    p = poly_from_int(235)
    res = Polynomial(2,1)
    res.set_irreducible_polynomial(irred8)
    p.set_irreducible_polynomial(irred8)
    for i in range(0,255):
        res = res*p
    assert (res==one)

    p = Polynomial(2,1,0,1)
    p.set_irreducible_polynomial(irred3)
    q = p.mult_inv()
    res = p*q
    assert(res == one)
    
    p = Polynomial(2,1,0,0,1,0,1,0,1)
    p.set_irreducible_polynomial(irred8)
    q = p.mult_inv()
    res = p*q
    assert(res == one)

    i = galois_inverse(228, irred8)
    res = galois_multiply(i,228,irred8)
    assert(res==1)
    
    i = galois_inverse(100, irred8)
    res = galois_multiply(i,100,irred8)
    assert(res==1)

    i = galois_inverse(1, irred8)
    res = galois_multiply(i,1,irred8)
    assert(res==1)


