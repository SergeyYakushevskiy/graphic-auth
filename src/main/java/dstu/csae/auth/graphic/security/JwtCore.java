package dstu.csae.auth.graphic.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureAlgorithm;
import io.jsonwebtoken.security.Keys;
import lombok.Getter;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Component;

import java.nio.charset.StandardCharsets;
import java.security.Key;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Date;

@Component
public class JwtCore {
    @Value("${app.secret}")
    private String secret;
    @Value("${app.secret.expirationMs}")
    @Getter
    private int lifetime;
    @Value("${app.2fa.expirationMs}")
    @Getter
    private int lifetime2Fa;

    private Key getSigningKey() {
        byte[] keyBytes = secret.getBytes(StandardCharsets.UTF_8);
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            keyBytes = digest.digest(keyBytes);
        }catch (NoSuchAlgorithmException ex){
            ex.printStackTrace();
        }
        return Keys.hmacShaKeyFor(keyBytes);
    }

    public String generate2FaToken(Authentication authentication){
        AccountDetailsImpl userDetails = (AccountDetailsImpl) authentication.getPrincipal();
        return Jwts.builder()
                .subject(userDetails.getIdentifier())
                .claim("purpose", "2fa")
                .issuedAt(new Date())
                .expiration(new Date(System.currentTimeMillis() + lifetime))
                .signWith(getSigningKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    public String generateToken(Authentication authentication){
        AccountDetailsImpl userDetails = (AccountDetailsImpl) authentication.getPrincipal();
        return Jwts.builder()
                .subject(userDetails.getIdentifier())
                .issuedAt(new Date())
                .expiration(new Date(System.currentTimeMillis() + lifetime))
                .signWith(getSigningKey(), SignatureAlgorithm.HS256)
                .compact();
    }

    public String getNameFromJwt(String token){
        return Jwts.parser()
                .setSigningKey(getSigningKey())
                .build()
                .parseClaimsJws(token)
                .getBody()
                .getSubject();
    }

    public Claims getClaims(String token) {
        return Jwts.parser()
                .setSigningKey(getSigningKey()) // secretKey = SecretKey или byte[]
                .build()
                .parseClaimsJws(token)
                .getBody();
    }


}
