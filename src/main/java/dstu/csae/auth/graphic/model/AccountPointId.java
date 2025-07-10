package dstu.csae.auth.graphic.model;

import java.io.Serializable;
import java.util.Objects;
import java.util.UUID;

// Класс для составного PK account_point
public class AccountPointId implements Serializable {
    private UUID account;
    private Integer x;
    private Integer y;

    public AccountPointId() {}

    public AccountPointId(UUID account, Integer x, Integer y) {
        this.account = account;
        this.x = x;
        this.y = y;
    }

    // equals и hashCode
    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof AccountPointId)) return false;
        AccountPointId that = (AccountPointId) o;
        return Objects.equals(account, that.account) &&
                Objects.equals(x, that.x) &&
                Objects.equals(y, that.y);
    }

    @Override
    public int hashCode() {
        return Objects.hash(account, x, y);
    }
}

